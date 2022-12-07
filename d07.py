from shared_use import read_file
from operator import itemgetter


class FileSystem:
    """
    FileSystem() --
    this class controls the data tree of inner class Directory()

    top - Directory() - the heed of the file system, in this case the root directory
        this assigns several items to the class Dictionary() upon __init__
        including Directory.name, Directory.dir_tree, and Directory.sup_dir

    self.on_disk - int() - the total size of the file system, defined on call to FileSystem.expand()
    self.free_space - int() - the free space on disk, defined on call to FileSystem.expand()

    functions:
    cd(self, str())
        changes self.current to a new subdirectory named in the str().
        this function will create a new Directory() item with FileSystem.mkdir() if the string passed is not
        already a subdirectory of the current directory before changing self.current.

        no return type

    mkdir(self, str())
        makes a new Directory() object named str() and ties it to it's parent directory

        no return type

    ls(self, list(), bool())
        both shows the contents of a directory and populates that directory
        this function needs the console log as a list() to create the items in each Directory() object
        it uses list.pop() and will remove items from the log as it moves across them. This funtion uses
        FileSustem.mkdir() and will append current.files if it finds new data, If the bool() is True
        then the function will end by printing the content of the directory to the console

        no return type

    expand(self, Directory(), int())
        recursive function
        this file shows an organized file system on the console, will also define FileSustem.on_disk and
        FileSystem.free_space when run. The free space is from an assumed 70,000,000 byte disk max.

        no return type

    mark_for_del(self, list(), Directory())
        recursive function
        this function loops the FileSustem object from top to identify space requirements for freeing
        disk space.
    """
    def __init__(self):
        print('Creating fresh file system')
        # create a base directory with name '/'
        self.top = self.Directory()
        self.top.name = '/'
        self.top.dir_tree = '/'
        # make the root directory reference itself when looking for super dir
        self.sup_dir = self.top
        # set the current directory to top
        self.current = self.top

        # file space variables
        self.on_disk = None
        self.free_space = None

    def cd(self, dir_name=None):
        # if no directory name provided
        if not dir_name:
            print('provide directory name')
            return

        # if returning to top
        if dir_name == '/':
            self.current = self.top
            return

        # if going one level up:
        if dir_name == '..':
            self.current = self.current.sup_dir
            return

        # if list of subdirs is empty
        if not self.current.sub_dir:
            print('empty dir, creating new subdir')
            self.mkdir(dir_name)

        # change dir from current subdir list
        for subs in self.current.sub_dir:
            if subs.name == dir_name:
                self.current = subs
                return

    def mkdir(self, dir_name=None):
        if not dir_name:
            print('provide directory name')
            return

        for subs in self.current.sub_dir:
            if subs.name == dir_name:
                print('directory already exists')
                return

        # make a new Directory obj
        new_dir = self.Directory()
        # give it the data we have
        new_dir.name = dir_name
        new_dir.dir_tree = f'{self.current.dir_tree}/{new_dir.name}'
        # tell it super is cur
        new_dir.sup_dir = self.current
        # tell cur it has a sub
        self.current.add_sub_dir(new_dir)
        return

    def ls(self, my_log, show=False):
        """
        ls in this case will also populate the file system if it
        finds files or directories that are not indexed already
        """
        # if there are items following our 'ls' command, we are adding, otherwise we are just looking
        if my_log:
            # loop though items to list, stopping at next shell command
            # check that my_log has items first to avoid indexing errors
            # that might come from popping last element
            while my_log and my_log[0][0] != '$':
                # grab the next line in our log
                my_item = my_log.pop(0)

                # if the item is not in the contents already, add it
                # if the item is a directory
                # and the name is not already in our subdir list
                if my_item.startswith('dir') and not any(my_item[4:] == a.name for a in self.current.sub_dir):
                    self.mkdir(my_item[4:])

                # if the item is not a directory
                # and the item is not in our files list
                else:
                    file_size, file_name = my_item.split(' ')
                    if [file_name, file_size] not in self.current.files:
                        self.current.files.append([file_name, file_size])

        if show:
            # list the contents of dir
            for item in self.current.sub_dir:
                # start with all directories, list name then D
                print(f' {item.name + " <DIR>" : <10}{item.give_size() : >10}')
            for item in self.current.files:
                # now list all files, list name then size
                print(f' {item[0] : <10}{item[1] : >10}')

    def expand(self, target=None, indent=0):
        # if we are at root, show total fs size
        if not target:
            target = self.top
            print('\n\n')
            # record variables in FileSystem
            self.on_disk = target.give_size()
            self.free_space = 70000000 - self.on_disk
            print(f'{self.on_disk} bytes on disk, {self.free_space} bytes of free space...\n')

        print(f'{"   " * indent}-{target.name+" <DIR>":<10}  {target.give_size():>10}')
        for files in target.files:
            print(f' {"   " * indent}| {files[0]:<10}{files[1]:>10}')
        for dirs in target.sub_dir:
            self.expand(dirs, indent + 1)

    def mark_for_del(self, dir_list, target=None):

        # if this is the first entry into loop, mark top as starting point
        if not target:
            target = self.top
        if not dir_list:
            dir_list = [[self.top.name, self.top.give_size()]]

        total_bytes = 0
        # look through the list of subdirectories
        for subs in target.sub_dir:
            # if the sub has subdirectories, recursively call function with new target
            if len(subs.sub_dir):
                total_bytes += self.mark_for_del(dir_list, subs)
            # if there are no subdirectories left to explore, get the size and check it
            this_size = subs.give_size()
            dir_list.append([subs.name, this_size])
            if this_size <= 100000:
                # print(f'i think {subs.name} is size {this_size}, adding for total of {total_bytes}')
                total_bytes += this_size

        if target == self.top:
            print(f'I think {total_bytes} bytes could be deleted for part 1.')

            dir_list = sorted(dir_list, key=itemgetter(1))

            needed = 30000000 - self.free_space
            print(f'You need {needed} to run properly...')
            for dirs in dir_list:
                if dirs[1] < needed:
                    continue
                else:
                    print(f'You should delete {dirs[0]} at {dirs[1]} bytes.')
                    break

        return total_bytes

    class Directory:
        """
        Directory() -- an inner class of FileSystem()
        this class holds the individual directories to move up and down our data tree

        name - str() - the name of the directory
        files - list() - a list of files and file sizes, each file is a sub-list [str(FILE NAME), str(FILE SIZE)]
        sub_dir - list() - a list of Directory() items, the contained subdirectories
        sup_dir - Directory() - a single Directory() item, the super-directory
        dir_tree - str() - the string of the directory tree

        functions:
        add_sub_dir(self, Directory())
            puts a Directory() into the list of sub_dir
            no return type

        get_size(self)
            returns the size of all files and subdirectories in this directory
            this call is recursive into all subdirectories
            return int()
        """
        def __init__(self):
            self.name = None
            self.files = []
            self.sub_dir = []
            self.sup_dir = None
            self.dir_tree = ''

        def add_sub_dir(self, new_dir=None):
            # make sure we got passed a name
            if not new_dir:
                print('cant add empty dir name')
            elif not isinstance(new_dir, FileSystem.Directory):
                print('cant add non-dir to subs')
            else:
                # append to list of Directory() types
                self.sub_dir.append(new_dir)

        def give_size(self):
            size = 0
            # look at all files contained
            for item in self.files:
                # add all the file sizes in
                size += int(item[1])
            # look at any subdirs
            for subs in self.sub_dir:
                size += subs.give_size()

            return size


def build_files(my_data):

    log = my_data.copy()
    fs = FileSystem()

    # continue loop while log has entries
    while log:
        # grab the current line
        current = log.pop(0)

        # print(f'${fs.current.dir_tree} {current[2:]}')

        # we only deal with the shell commands, so look which one
        if '$ cd' in current:
            # the name of the dir to change to will start at index 5 in the string
            fs.cd(current[5:])
            continue
        elif '$ ls' in current:
            # pass the current log to the fs.ls function, it will pop values as it lists
            fs.ls(log)
            continue
        else:
            print('Ooops! I can\'t find a command!')
            print('exiting...')
            return

    fs.expand()
    fs.mark_for_del([])


def main():
    raw_data = read_file('d07')
    print(raw_data)

    build_files(raw_data)


if __name__ == '__main__':
    print('running day 7')
    main()
