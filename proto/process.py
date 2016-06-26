import struct


debit_type = 'debit'
credit_type = 'credit'
start_auto_type = 'start_auto'
end_auto_type = 'end_auto'
record_types = {
    '\x00': debit_type,
    '\x01': credit_type,
    '\x02': start_auto_type,
    '\x03': end_auto_type,
}
checked_user_id = 2456938384156277127


def process():
    path = 'txnlog.dat'
    debit_dollars = 0.0
    credit_dollars = 0.0
    started_autopays = 0
    ended_autopays = 0
    user_balance = 0
    with open(path, 'r') as f:
        _, _, num = read_header(f)
        for i in range(num):
            record_type, timestamp, user_id, amount = read_record(f)
            if record_type == debit_type:
                debit_dollars += amount
                if user_id == checked_user_id:
                    user_balance += amount
            if record_type == credit_type:
                credit_dollars += amount
                if user_id == checked_user_id:
                    user_balance -= amount
            if record_type == start_auto_type:
                started_autopays += 1
            if record_type == end_auto_type:
                ended_autopays += 1
            print('Record Type: {}, Time: {}, UserId: {}, Amount: {}'
                  .format(record_type, timestamp, user_id, amount))
    show_answers(debit_dollars, credit_dollars, started_autopays, ended_autopays, user_balance)


def read_header(f):
    magic_string = f.read(4)
    version = ord(f.read(1))
    number_of_records, = struct.unpack('!I', f.read(4))
    return magic_string, version, number_of_records


def read_record(f):
    record_type = record_types[f.read(1)]
    timestamp, = struct.unpack('!I', f.read(4))
    user_id, = struct.unpack_from('!Q', f.read(8))
    amount = None
    if record_type in [debit_type, credit_type]:
        amount, = struct.unpack_from('!d', f.read(8))
    return record_type, timestamp, user_id, amount


def show_answers(debit, credit, started, ended, balance):
    questions = {
        'What is the total amount in dollars of debits?': debit,
        'What is the total amount in dollars of credits?': credit,
        'How many autopays were started?': started,
        'How many autopays were ended?': ended,
        'What is balance of user ID 2456938384156277127?': balance
    }
    for question, answer in questions.iteritems():
        print('{} {}'.format(question, answer))

if __name__ == '__main__':
    process()
