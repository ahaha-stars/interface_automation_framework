def generate_model_id():

    for i in range(1,1000):
        model_id = 'M' + str(i).zfill(2) + '_'
        yield model_id

def generate_testcase_id():
    for i in range(1,10000):
        case_id = str(i).zfill(2) + '_'
        yield case_id

model_id = generate_model_id()
case_id = generate_testcase_id()
