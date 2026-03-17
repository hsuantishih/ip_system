from sqlalchemy import func, Integer
from admin.models import Host, Allocation
from app import db
import ipaddress


class IPCalculator:
    # 生成 ip_min to ip_max
    def generate_ip_range(self, host_min, host_max, host_id):
        min_ip = ipaddress.ip_address(str(host_min))
        max_ip = ipaddress.ip_address(str(host_max))

        current_ip = min_ip
        while current_ip <= max_ip:
            print(current_ip)
            host_allocation = Allocation(ip=current_ip, host_id=host_id)
            db.session.add(host_allocation)
            current_ip += 1

        db.session.commit()

    # 替換 ip 第四個位元組
    def replace_last_octet(self, ip_str, new_octet):
        ip = ipaddress.IPv4Address(ip_str)
        new_ip = ipaddress.IPv4Address(int(ip) & 0xFFFFFF00 | new_octet)

        return str(new_ip)

    # 生成 ip group，從 host_min 開始生成之後的 group
    def generate_ip_group(
        self, host_min, host_max, subnet, host_deptname, comment, host_users
    ):
        # 整理資料
        host_min_class = host_min.split(".")
        host_type = ".".join(host_min_class[:2])
        host_class_c = "." + host_min_class[2]
        host_min_data = int(host_min_class[3])
        host_max_data = int(host_max.split(".")[-1])

        # 設定參數 & group 的起點
        bit_num = 2 ** (32 - int(subnet))
        itr = host_min_data - 1  # Network Address
        end = host_max_data + 2  # Next Network Address
        count = itr // bit_num + 1
        current = host_min

        while itr != end:
            current = self.replace_last_octet(current, itr)
            network = ipaddress.IPv4Network(f"{current}/{subnet}", strict=False)

            network_hosts = [host for host in network.hosts()]

            host_min = network_hosts[0]
            host_max = network_hosts[-1]

            # 將 type, class_c, min, max 拆出來
            host_class = str(host_min).split(".")
            host_type = ".".join(host_class[:2])
            host_class_c = "." + host_class[2]
            host_min = "." + host_class[3]
            host_class = str(host_max).split(".")
            host_max = "." + host_class[3]
            host_len = int(host_max[1:]) - int(host_min[1:]) + 1

            # 計算 Gateway
            gateway = "." + str(int(host_class[3]) - 1)

            print(f"-------Group{count}-------")
            print("HostType  Address:", host_type)
            print("Class_C   Address:", host_class_c)
            print("HostMin   Address:", host_min)
            print("HostMax   Address:", host_max)
            print("Gateway   Address:", gateway)
            print("Subnet           :", subnet)
            print("Avaliable    Host:", host_len)
            print("Netmask   Address:", network.netmask)
            print("Network   Address:", network.network_address)
            print("Broadcast Address:", network.broadcast_address)

            # 建立資料
            new_host = Host(
                host_type=host_type,
                host_class_c=host_class_c,
                host_min=host_min,
                host_max=host_max,
                host_len=host_len,
                gateway=gateway,
                subnet=subnet,
                netmask=network.netmask,
                host_deptname=host_deptname,
                comment=comment,
            )

            # 存入資料庫
            db.session.add(new_host)
            db.session.commit()

            for user in host_users:
                new_host.users.append(user)
                db.session.commit()

            # 生成 host_allocation 資料
            host_min = new_host.host_type + new_host.host_class_c + new_host.host_min
            host_max = new_host.host_type + new_host.host_class_c + new_host.host_max
            host_id = new_host.id

            # 使用函數
            self.generate_ip_range(
                host_min=host_min, host_max=host_max, host_id=host_id
            )

            print(itr, end)
            itr += bit_num
            count += 1
            print(itr, end)

    # 檢查取得的資料；input 為 form data: 數值沒有 "."
    def check_for_db(self, hostform_type, hostform_class_c, hostform_min, hostform_max):
        # 回傳資料
        data = {}

        # 查詢資料庫: data 在資料庫裡
        exist_host = Host.query.filter_by(
            host_type=hostform_type,
            host_class_c="." + hostform_class_c,
            host_min="." + hostform_min,
            host_max="." + hostform_max,
            deleted=False,
        ).first()

        if exist_host:
            print(f"form_data 是資料庫的 {exist_host}")

            data["status"] = "exist"
            data["host_list"] = [exist_host]

            return data

        # 不在資料庫 -> 查詢資料庫: 符合 host_type & host_class_c
        # 回傳資料:[h_1, h_2, ..., h_n], where ∪h_i = 1 ~ 254
        # h_i 聯集: 140.116.1.1 ~ 140.116.1.254
        correspond_host_list = (
            Host.query.filter_by(
                host_type=hostform_type,
                host_class_c="." + hostform_class_c,
                deleted=False,
            )
            .order_by(func.substring(Host.host_min, 2).cast(Integer))
            .all()
        )

        print(correspond_host_list)

        print(hostform_min, hostform_max)

        # 整理參數
        hostform_len = int(hostform_max) - int(hostform_min) + 1

        # 檢查資料
        for host in correspond_host_list:
            # 整理資料庫的資料
            host_len = host.host_len
            host_min = int(host.host_min[1:])
            host_max = int(host.host_max[1:])

            # F 是 h_i 的子節點
            if host_len > hostform_len:
                # h_i.min == F.min
                match_min_condition = host_min == int(hostform_min)
                # h_i.max == F.max
                match_max_condition = host_max == int(hostform_max)
                # h_i.min < F.min and F.max < h_i.max
                include_condition = (host_min < int(hostform_min)) and (
                    int(hostform_max) < host_max
                )

                if match_min_condition or match_max_condition or include_condition:
                    parent_host = host
                    print(f"form_data 是 {parent_host} 的子節點")

                    data["status"] = "split"
                    data["host_list"] = [parent_host]

                    # 回傳父節點
                    return data

            # F 是 h_i 的父節點
            elif host_len < hostform_len:
                # 存在 i, j 使得 h_i.min == F.min and h_j == F.max
                # where i != j -> 找到 i 後往後找

                # h_i.min == F.min
                match_min_condition = host_min == int(hostform_min)

                print(f"len: {host_len} {hostform_len}")
                print(f"min: {host_min} {hostform_min}")

                if match_min_condition:
                    # 取得當前 host 在 list 的 index
                    current_index = correspond_host_list.index(host)

                    print(f"成功找到 {current_index} 在 {correspond_host_list}")

                    # 找 i 以後的 j
                    for remain_host in correspond_host_list[current_index + 1 :]:
                        # 整理參數
                        remain_host_max = int(remain_host.host_max[1:])

                        print(f"max: {remain_host_max} {hostform_max}")

                        # h_j == F.max
                        match_max_condition = remain_host_max == int(hostform_max)

                        if match_max_condition:
                            last_index = correspond_host_list.index(remain_host)

                            print(f"成功進到 max match {last_index}")

                            child_hosts = correspond_host_list[
                                current_index : last_index + 1
                            ]

                            print(f"form_data 是 {child_hosts} 的父節點")

                            data["status"] = "merge"
                            data["host_list"] = child_hosts

                            # 回傳子節點的 list
                            return data