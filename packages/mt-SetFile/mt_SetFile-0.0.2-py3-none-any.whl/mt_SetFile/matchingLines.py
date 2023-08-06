def lines_that_equal(line_to_match, fp):
    return [line for line in fp if line == line_to_match]

def lines_that_contain(string, fp):
    return [line for line in fp if string in line]

def lines_that_start_with(string, fp):
    return [line for line in fp if line.startswith(string)]

def lines_that_end_with(string, fp):
    return [line for line in fp if line.endswith(string)]
	
	
#Build generator of matched lines (memory efficient):

def generate_lines_that_equal(string, fp):
    for line in fp:
        if line == string:
            yield line

#Print all matching lines (find all matches first, then print them):

with open("file.txt", "r") as fp:
    for line in lines_that_equal("my_string", fp):
        print line

#Print all matching lines (print them lazily, as we find them)

with open("file.txt", "r") as fp:
    for line in generate_lines_that_equal("my_string", fp):
        print line
