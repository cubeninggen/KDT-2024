students = [('Alice', 3.9, 20160303),
            ('Bob', 3.0, 20160302),
            ('Charlie', 4.3, 20160301)]
# 학번(students[2])을기준으로오름차순정렬
sorted_students1 = sorted(students, key = lambda s: s[2])
print(sorted_students1)
# 학점(students[1])을기준으로내림차순정렬
sorted_students2 = sorted(students, key = lambda s: s[1], reverse=True)
print(sorted_students2)