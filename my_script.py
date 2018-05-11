import sys
import json

# print('python running from nodeJS')
# print "\n".join(sys.argv)

#Read data from stdin
def read_in():
    # lines = sys.stdin.readlines()
    load = sys.stdin.read()
    # Since our input would only be having one line, parse our JSON data from that
    # return json.loads(lines[0])
    return json.loads(load)
    # return json.dumps(load)
    # return lines
    # return load

def main():
    #get our data as an array from read_in()
    # output = read_in()
    # print(json.dumps(output))
    print('test output from python script!')

    # sys.stdout.write(lines)

    # Sum  of all the items in the providen array
    # total_sum_inArray = 0
    # for item in lines:
        # total_sum_inArray += item

    #return the sum to the output stream
    # print total_sum_inArray


# Start process
if __name__ == '__main__':
    main()


