from pydantic import BaseModel
from datetime import datetime
import colorama


class log(BaseModel):
    ''' log data model '''

    date: datetime
    level: str
    mod_id: str  # module id
    description: str  # log content


def format_log(log_obj: log):
    # color log levels
    log_tag_color_map = {
        'ERROR': f"{colorama.Back.RED}[ERROR]{colorama.Style.RESET_ALL}",
        'INFO': '[INFO]',
        'DEBUG': '[DEBUG]',
    }

    return f"[{log_obj.date.strftime('%Y-%m-%d %H:%M:%S')}] {log_tag_color_map[log_obj.level]} [{log_obj.mod_id}] | {log_obj.description}"


def print_log(mod_id: str, level: str, desc: str):
    temp_log_obj = log(
        date=datetime.now(),
        level=level,
        mod_id=mod_id,
        description=desc
    )

    formated_log = format_log(temp_log_obj)

    print(formated_log)
