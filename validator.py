import csv
from csv import DictReader

from usps import USPSApi, Address

# Add a valid USPS API key here, get this from https://registration.shippingapis.com/
usps = USPSApi('XXXXXXXXXXX', test=False)
validated_addr = {}


def createAddressLine():
    validated_addr[row["Employee ID"]] = {'User ID': row["User ID"],
                                          'First Name': row["First Name"],
                                          'Last Name': row["Last Name"],
                                          'Employee ID': row["Employee ID"],
                                          'City': address["City"],
                                          'Address1': address["Address1"],
                                          'Address2': address["Address2"],
                                          'State': address["State"], 'Zip5': address["Zip5"],
                                          'Zip4': address["Zip4"]}


def createAddressErrorLine():
    validated_addr[row["Employee ID"]] = {'User ID': row["User ID"],
                                          'First Name': row["First Name"],
                                          'Last Name': row["Last Name"],
                                          'Employee ID': row["Employee ID"],
                                          'City': row["City"],
                                          'Address1': row["Address 1"],
                                          'Address2': '',
                                          'State': row["State"], 'Zip5': row["Zip Code"],
                                          'Zip4': 'ERROR'}


with open('empire_driverlist_test.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)  # type: DictReader
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        address = Address(
            name='{row["First Name"]} {row["Last Name"]}',
            address_1=row["Address 1"],
            city=row["City"],
            state=row["State"],
            zipcode=row["Zip Code"]
        )

        try:
            validation = usps.validate_address(address)
            addressV = validation.result["AddressValidateResponse"]
            address = addressV["Address"]

            if 'Error' not in address:
                createAddressLine()
            else:
                createAddressErrorLine()

        except:
            createAddressErrorLine()

        print(address)



        line_count += 1

with open('empire_driverlist_validated_temp.csv', mode='w') as csv_filew:
    fieldnames = ['User ID', 'Employee ID', 'First Name', 'Last Name', 'City', 'Address1', 'Address2', 'State', 'Zip5',
                  'Zip4']
    writer = csv.DictWriter(csv_filew, fieldnames=fieldnames)
    writer.writeheader()

    for key, addr in validated_addr.items():
        writer.writerow({'User ID': addr["User ID"], 'First Name': addr["First Name"],
                         'Last Name': addr["Last Name"], 'Employee ID': addr["Employee ID"],
                         'City': addr["City"], 'Address1': addr["Address1"], 'Address2': addr["Address2"],
                         'State': addr["State"], 'Zip5': addr["Zip5"], 'Zip4': addr["Zip4"]})
