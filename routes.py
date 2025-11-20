# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from googlegenai import ask_gemini
from models import get_all_events, get_event_by_id, add_event, toggle_complete, update_event, get_db_connection
from utils import format_time, format_event_time, format_event_date, is_event_completed
from datetime import datetime
import pytz

VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')
main_bp = Blueprint('main', __name__, template_folder='templates')

# === TRANG CHỦ ===
@main_bp.route('/', methods=['GET', 'POST'])
def index():
    filter_type = request.args.get('filter', 'all')
    show_form = request.args.get('add') == '1'
    now = datetime.now(VN_TZ)

    # Xử lý thêm sự kiện
    if request.method == 'POST' and 'add_event' in request.form:
        event_name = request.form['eventName'].strip()
        start_time = request.form['startTime']
        end_time = request.form.get('endTime', '')
        location = request.form['location'].strip()
        reminder_minutes = int(request.form.get('reminderMinutes', 0))

        if not event_name or not start_time:
            flash('Vui lòng nhập tên và thời gian!', 'error')
        else:
            new_id = add_event(event_name, start_time, end_time or None, location or None, reminder_minutes)
            if new_id:
                flash('Thêm sự kiện thành công!', 'success')
            else:
                flash('Thời gian không hợp lệ!', 'error')
        return redirect(url_for('main.index', filter=filter_type))

    # Xử lý đánh dấu hoàn thành
    if request.method == 'POST' and 'toggle_complete' in request.form:
        event_id = request.form['event_id']
        toggle_complete(event_id)
        return redirect(url_for('main.index', filter=filter_type))

    # Lấy danh sách sự kiện
    all_events = get_all_events()
    filtered_events = []
    for e in all_events:
        completed = is_event_completed(e, now)
        if filter_type == 'all' or \
           (filter_type == 'upcoming' and not completed) or \
           (filter_type == 'completed' and completed):
            filtered_events.append({
                'id': e['id'],
                'name': e['event'],
                'date': format_event_date(e['start_time']),
                'time': format_event_time(e['start_time'], e['end_time']),
                'location': e['location'] or 'Không có địa điểm',
                'reminder_minutes' : e['reminder_minutes'],
                'completed': completed
            })

    return render_template('index.html',
                           events=filtered_events,
                           filter=filter_type,
                           selected_datetime=request.args.get('datetime', '').replace(' ', 'T')[:16],
                           show_form=show_form,
                           format_time=format_time)

# === XEM CHI TIẾT ===
@main_bp.route('/view/<int:event_id>')
def view_event_detail(event_id):
    event = get_event_by_id(event_id)
    if not event:
        flash('Sự kiện không tồn tại!', 'error')
        return redirect(url_for('main.index'))

    formatted = {
        'id': event['id'],
        'name': event['event'],
        'start_time': datetime.fromisoformat(event['start_time']).strftime('%Y-%m-%dT%H:%M'),
        'end_time': datetime.fromisoformat(event['end_time']).strftime('%Y-%m-%dT%H:%M') if event['end_time'] else None,
        'location': event['location'] or '',
        'reminder_minutes': event['reminder_minutes'],
        'created_at': event['created_at']
    }

    return render_template('index.html',
                           detail_event=formatted,
                           filter=request.args.get('filter', 'all'),
                           format_time=format_time)

# === CHỈNH SỬA ===
@main_bp.route('/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event_detail(event_id):
    event = get_event_by_id(event_id)
    if not event:
        flash('Sự kiện không tồn tại!', 'error')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        name = request.form['eventName'].strip()
        start = request.form['startTime']
        end = request.form['endTime']
        location = request.form['location'].strip()
        reminder = int(request.form.get('reminderMinutes', 0))

        if update_event(event_id, name, start, end, location, reminder):
            flash('Cập nhật thành công!', 'success')
        else:
            flash('Dữ liệu không hợp lệ!', 'error')
        return redirect(url_for('main.view_event_detail', event_id=event_id, filter=request.args.get('filter', 'all')))

    # GET: hiển thị form sửa
    formatted = {
        'id': event['id'],
        'name': event['event'],
        'start_time': datetime.fromisoformat(event['start_time']).strftime('%Y-%m-%dT%H:%M'),
        'end_time': datetime.fromisoformat(event['end_time']).strftime('%Y-%m-%dT%H:%M') if event['end_time'] else None,
        'location': event['location'] or '',
        'reminder_minutes': event['reminder_minutes']
    }

    return render_template('index.html',
                           edit_event=formatted,

                           filter=request.args.get('filter', 'all'),
                           format_time=format_time)


# === API CHAT AI ===
@main_bp.route('/api/chat', methods=['POST'])
def chat_ai():
    """API endpoint để chat với AI và tạo sự kiện"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'error': 'Tin nhắn không được để trống'}), 400

        # Gọi hàm ask_gemini
        ai_response = ask_gemini(user_message)

        if ai_response['event'] is None:
            return jsonify({
                'success': False,
                'message': 'Cung cấp tên sự kiện'
            })

        if ai_response['start_time'] is None:
            return jsonify({
                'success': False,
                'message': 'Cung cấp thời gian sự kiện'
            })

        # Kiểm tra nếu AI trả về dữ liệu sự kiện hợp lệ
        if ai_response and ai_response.get('event'):
            # Tự động thêm sự kiện vào database
            new_id = add_event(
                ai_response['event'],
                ai_response['start_time'],
                ai_response['end_time'],
                ai_response['location'],
                ai_response['reminder_minutes']
            )

            if new_id:
                return jsonify({
                    'success': True,
                    'message': f'✓ Đã tạo sự kiện: {ai_response["event"]}',
                    'event': ai_response,
                    'event_id': new_id
                })
            else:
                return jsonify({
                    'success': False,
                    'message': '✗ Thời gian không hợp lệ, vui lòng thử lại'
                })
        else:
            return jsonify({
                'success': False,
                'message': 'Xin lỗi, tôi không hiểu yêu cầu của bạn. Hãy thử: "Tạo cuộc họp vào 9h sáng mai"'
            })

    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500


# === TÌM KIẾM SỰ KIỆN ===
@main_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    filter_type = request.args.get('filter', 'all')

    all_events = get_all_events()
    now = datetime.now(VN_TZ)

    results = []
    for e in all_events:
        if query.lower() in e['event'].lower() or query in (e['location'] or ''):
            completed = e['isComplete'] == 1 or (e['end_time'] and datetime.fromisoformat(e['end_time']) < now)
            if filter_type == 'all' or \
                    (filter_type == 'upcoming' and not completed) or \
                    (filter_type == 'completed' and completed):
                results.append({
                    'id': e['id'],
                    'name': e['event'],
                    'date': format_event_date(e['start_time']),
                    'time': format_event_time(e['start_time'], e['end_time']),
                    'location': e['location'] or 'Không có địa điểm',
                    'completed': completed
                })

    return render_template('index.html',
                           events=results,
                           filter=filter_type,
                           now=now,
                           search_query=query,
                           format_time=format_time)


@main_bp.route('/filter-date')
def filter_by_date():
    datetime_str = request.args.get('datetime')  # Lấy từ input datetime-local
    filter_type = request.args.get('filter', 'all')

    all_events = get_all_events()
    now = datetime.now(VN_TZ)
    filtered = []

    # Nếu có chọn ngày giờ → lọc theo ngày (không cần giờ chính xác)
    target_date = None
    if datetime_str:
        try:
            target_date = datetime.fromisoformat(datetime_str.replace('T', ' ')).date()
        except:
            target_date = None

    for e in all_events:
        event_date = datetime.fromisoformat(e['start_time']).date()

        # Nếu có lọc ngày → chỉ hiển thị sự kiện cùng ngày
        if target_date and event_date != target_date:
            continue

        completed = e['isComplete'] == 1 or (e['end_time'] and datetime.fromisoformat(e['end_time']) < now)
        if filter_type in ('all', '') or \
                (filter_type == 'upcoming' and not completed) or \
                (filter_type == 'completed' and completed):
            filtered.append({
                'id': e['id'],
                'name': e['event'],
                'date': format_event_date(e['start_time']),
                'time': format_event_time(e['start_time'], e['end_time']),
                'location': e['location'] or 'Không có địa điểm',
                'completed': completed
            })

    # Truyền lại giá trị đã chọn để input giữ nguyên
    selected_datetime = datetime_str.replace(' ', 'Tovel') if datetime_str else ''

    return render_template('index.html',
                           events=filtered,
                           filter=filter_type,
                           selected_datetime=selected_datetime[:16],  # Chỉ lấy phần YYYY-MM-DDTHH:MM
                           format_time=format_time)

# === XÓA SỰ KIỆN ===
@main_bp.route('/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()
    flash('Đã xóa sự kiện!', 'success')
    return redirect(url_for('main.index'))