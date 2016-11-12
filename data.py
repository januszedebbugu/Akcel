def data_to_list(data, ts, data_list):
    acX = ((data[0] << 8) | data[1])
    acY = ((data[2] << 8) | data[3])
    acZ = ((data[4] << 8) | data[5])
    data_tuple = (ts, acX, acY, acZ)
    print(data_tuple)
    if len(data_list) == 100:
        del data_list[0]
    data_list.append(data_tuple)
