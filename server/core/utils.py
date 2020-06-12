from core.models import *
from simple_history.models import HistoricalRecords


def get_ahj_diff(ahj):
    new_record = ahj.history.first()
    old_record = ahj.history.first()
    if new_record is None:
        new_record = old_record
    delta = new_record.diff_against(old_record)
    for change in delta.changes:
        print("{} changed from {} to {}".format(change.field, change.old, change.new))
