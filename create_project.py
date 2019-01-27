import os


# Each site crawled will create a new directory
def create_project_directory(directory):
    if not os.path.exists(directory):
        print('Creating new directory for Site: ' + directory)
        os.makedirs(directory)


# Create queued and crawled files (if not already created)
def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


# Write a new File
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


# Call the function for testing purposes
# create_data_files(project_name, base_url)

# Add data to an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


# Delete the contents of a File
def delete_file_content(path):
    open(path, 'w').close()


# Create a Set so that unique values are stored then periodically write to file.

# Read File and convert each line into a Set item
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set and convert each line to text file
def set_to_file(links, file_name):
    with open(file_name, 'w') as f:
        for l in sorted(links):
            f.write(l + '\n')
