# 跨服填玩家uid，本服可以用username

def generate_timestamps(start, end, step):
    # 生成指定间隔的时间戳列表
    return list(range(start, end, step))

def combine_uids_with_timestamps(uids, timestamps):
    # 将用户ID与时间戳结合，并返回逗号分隔的字符串
    combined_list = [f"{uid},{timestamp}" for uid, timestamp in zip(uids, timestamps)]
    return ",".join(combined_list)

def print_combined_uids_and_timestamps(uids_title, uids, timestamps):
    # 打印用户ID和时间戳的组合
    print(f"{uids_title}:")
    output_string = combine_uids_with_timestamps(uids, timestamps)
    print(output_string)

# 5服联盟Icu的用户ID
uids = ['饺子没皮', '樱桃', '嗷嗷', '面包', 'kn13', '活动10 ', '夹心饼干']
# 5服联盟DVR的用户ID
uids1 = ['酸辣粉', '泡馍', '滴滴11', 'gs1', '解锁3', 'GX001']
# 22联盟UNT的用户ID
uids2 = ['AAAA', 'CN苹果', 'gs2', 'ONE1', 'per', 'per4']

# 定义时间戳的起始、结束和步长
start_timestamp = 30
end_timestamp = 10
step = -3

# 生成时间戳列表
timestamps = generate_timestamps(start_timestamp, end_timestamp, step)

# 打印5服联盟Icu的用户ID和时间戳
print_combined_uids_and_timestamps("5服联盟Icu", uids, timestamps)

# 打印5服联盟DVR的用户ID和时间戳
print_combined_uids_and_timestamps("5服联盟DVR", uids1, timestamps)

# 打印22联盟UNT的用户ID和时间戳
print_combined_uids_and_timestamps("22联盟UNT", uids2, timestamps)