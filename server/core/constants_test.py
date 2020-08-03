EDIT_SUBMIT_ENDPOINT = '/api/v1/edit/submit/'
EDIT_DETAIL_ENDPOINT_CONFIRM = lambda pk, status: '/api/v1/edit/%i/?confirm=%s' % (pk, status)
EDIT_DETAIL_ENDPOINT_VOTE = lambda pk, rating: '/api/v1/edit/%i/?vote=%s' % (pk, rating)

EDIT_CREATE_AHJ = {'RecordType': 'AHJ', 'EditType': 'create'}
EDIT_CREATE_ADDRESS = lambda ParentID, ParentRecordType: {'RecordType': 'Address', 'ParentID': ParentID, 'ParentRecordType': ParentRecordType, 'EditType': 'create'}
EDIT_CREATE_CONTACT = lambda ParentID: {'RecordType': 'Contact', 'ParentID': ParentID, 'ParentRecordType': 'AHJ', 'EditType': 'create'}
EDIT_CREATE_ENG_REV_REQ = lambda ParentID: {'RecordType': 'EngineeringReviewRequirement', 'ParentID': ParentID, 'ParentRecordType': 'AHJ', 'EditType': 'create'}
EDIT_CREATE_LOCATION = lambda ParentID: {'RecordType': 'Location', 'ParentID': ParentID, 'ParentRecordType': 'Address', 'EditType': 'create'}

EDIT_DELETE = lambda RecordID, RecordType: {'RecordID': RecordID, 'RecordType': RecordType, 'EditType': 'delete'}

EDIT_UPDATE = lambda RecordID, RecordType, FieldName, Value: {'RecordID': RecordID, 'RecordType': RecordType, 'EditType': 'update', 'FieldName': FieldName, 'Value': Value}
