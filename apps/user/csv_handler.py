from app import db
from admin.models import Allocation
import csv, uuid, os, io

class CsvHandler:
    def __init__(self):
        self.dirname = os.path.join("user", "csv_files")
        self.csv_fieldnames = ['Ip', 'Mac', 'Owner', 'Comment', 'Device']

    # 隨機檔名
    def generate_csv_name(self):
        self.csv_uuid = str(uuid.uuid4())

        return self.csv_uuid

    # 生成對應的host_allocation到csv
    def create_initial_data(self, host):

        csv_file_name = self.generate_csv_name()
        csv_path_name = os.path.join(self.dirname, csv_file_name + ".csv")

        csvfile = open(csv_path_name, newline="", encoding='utf-8-sig', mode="w")

        writer = csv.DictWriter(csvfile, fieldnames=self.csv_fieldnames)

        writer.writeheader()

        for host_allocation in host.host_allocation:

            allocation_dict = {
                'Ip': host_allocation.ip,
                'Mac': host_allocation.mac,
                'Owner': host_allocation.owner,
                'Comment': host_allocation.comment,
                'Device': host_allocation.device,
                }
            
            if allocation_dict['Device'] == "請選擇設備":
                allocation_dict['Device'] = ""
            
            writer.writerow(allocation_dict)

        csvfile.close()

        return csv_path_name, csv_file_name + ".csv"

    def insert_csv_data(self, file, host_id):
        try:
            text_wrapper = io.TextIOWrapper(file, encoding="utf-8-sig")
            reader = csv.reader(text_wrapper)

            next(reader)

            for row in reader:
                host_allocation = Allocation.query.filter_by(
                    host_id=host_id,
                    ip=row[0]
                ).first()

                host_allocation.mac = row[1]
                host_allocation.owner = row[2]
                host_allocation.comment = row[3]
                host_allocation.device = row[4]

            db.session.commit()

            return True

        except:
            return False
