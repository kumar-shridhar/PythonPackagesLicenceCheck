
import pkg_resources
import prettytable
import csv
import re

def get_pkg_license(pkg):
    try:
        lines = pkg.get_metadata_lines('METADATA')
    except:
        lines = pkg.get_metadata_lines('PKG-INFO')

    for line in lines:
        if line.startswith('License:'):
            return line[9:]
    return '(Licence not found)'

def write_packages_and_licenses():
    t = prettytable.PrettyTable(['Package', 'Licence'])
    for pkg in sorted(pkg_resources.working_set, key=lambda x: str(x).lower()):
        t.add_row((str(pkg), get_pkg_license(pkg)))

    with open("licence.txt", "w") as text_file:
        text_file.write(str(t))

    with open("licence.csv", "w") as csv_write_file:
        fieldnames = ['Package', 'Licence']
        licence_writer = csv.DictWriter(csv_write_file, delimiter='\t', fieldnames = fieldnames)
        licence_writer.writeheader()
        for pkg in sorted(pkg_resources.working_set, key=lambda x: str(x).lower()):
            licence_writer.writerow({'Package':str(pkg), 'Licence':get_pkg_license(pkg) })

def check_package_status():
    with open('licence.csv', 'r') as csv_read_file:
        licence_reader = csv.DictReader(csv_read_file, delimiter='\t')
        for line in licence_reader:
            if re.search('(GNU|GPL)',line['Licence']):
                print ('The {} Package is using a Copy left licence and please replace it'.format(line['Package']))

def main():
    write_packages_and_licenses()
    check_package_status()

if __name__=='__main__':
    main()

