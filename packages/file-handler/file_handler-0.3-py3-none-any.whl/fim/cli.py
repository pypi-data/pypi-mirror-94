import os
import shutil
import click

@click.command()
@click.option('--retain','-r', is_flag=True, help="Retain original files")
@click.option('--pack','-p', is_flag=True, help="Package into organized folder")
def main(retain=False,pack=False):
    confirmation = input('The files in the current folder ('+os.getcwd()+') will be organized.\nDisplacement of files may affect programs in which the file is already opened/is in use.\nProceed? (y/n):')
    if confirmation.lower()=='y':
        with os.scandir(os.getcwd()) as dir_entries:
            file_list = [file for file in dir_entries if not os.path.isdir(file.path)]
        file_grouping(file_list,retain,pack)
    elif confirmation.lower()=='n':
        print('Understandable. Have a nice day.')
    else:
        print('Invalid input.')


def file_grouping(file_list,retain,pack):
    for file in file_list:
        destination = os.getcwd()
        if pack:
            destination = os.path.join(os.getcwd(),'Organized')
            if not os.path.isdir(destination):
                os.mkdir(destination)
        destination = os.path.join(destination,file.name.split('.')[-1])
        if os.path.isdir(destination):
            if not retain:
                print('Moving file ',file.name,' to ',destination)
                shutil.move(file.path,destination)
            else:
                print('Copying file ',file.name,' to ',destination)
                shutil.copy(file.path,destination)
        else:
            if not retain:
                os.mkdir(destination)
                print('Moving file ',file.name,' to ',destination)
                shutil.move(file.path,destination)
            else:
                os.mkdir(destination)
                print('Copying file ',file.name,' to ',destination)
                shutil.copy(file.path,destination)

if __name__=='__main__':
    main()