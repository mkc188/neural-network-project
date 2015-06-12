import sys

if __name__ == "__main__":
    rawdata = open(sys.argv[1])
    dataset = open(sys.argv[2], mode='w')
    answer = open(sys.argv[3], mode='w')

    for d_line in rawdata:
        d_line = d_line.rstrip().replace(',', '')
        for c in d_line[:-1]:
            if c == '0':
                dataset.write('0 ')
            elif c == '1':
                dataset.write('1 ')
            elif c == '2':
                dataset.write('2 ')
            else:
                dataset.write('3 ')
        dataset.write('\n')

        if d_line[-1:].isdigit():
            answer.write(d_line[-1:] + '\n')
        else:
            answer.write('?')

    rawdata.close()
    dataset.close()
    answer.close()
