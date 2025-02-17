contry_list={'Seoul':['South Korea','Asia',9655000],
             'Tokyo':['Japan','Asia',14110000],
             'Beijing':['China','Asia',21540000],
             'London':['United Kingdome','Europe',14800000],
             'Berlin':['Germany','Europe',3426000],
             'Mexico City':['Mexico','America',21200000]}
def main():
    while True:
        print('-----------------------------------------')
        print('1. 전체 데이터 출력')		
        print('2. 수도 이름 오름차순 출력')											
        print('3. 모든 도시의 인구수 내림차순 출력')		
        print('4. 특정 도시의 정보 출력')		
        print('5. 대륙별 인구수 계산 및 출력')		
        print('6. 프로그램 종료')
        print('-----------------------------------------')
        menu_num=int(input('메뉴를 입력하세요: '))
        if menu_num==1:
            _=1
            for i,j in contry_list.items():
                print(f'[{_}] {i}: {j}')
                _+=1
        elif menu_num==2:
            _=1
            for i in sorted(contry_list.keys()):
                print(f'[{_}] {i:<15}: {contry_list[i][0]:<15} {contry_list[i][1]:<10} {contry_list[i][2]:>10,}')
                _+=1
        elif menu_num==3:
            _=1
            for i in sorted(contry_list.items(),key=lambda x:x[1][2],reverse=True):
                print(f'[{_}] {i[0]:<15}: {i[1][2]:>10,}')
                _+=1
        elif menu_num==4:
            city=input('출력할 도시 이름을 입력하세요: ')
            if city in contry_list.keys():
                print(f'도시:{city}')
                print(f'국가:{contry_list[city][0]}, 대륙:{contry_list[city][1]}, 인구수:{contry_list[city][2]}')
            else:
                print(f'도시이름: {city}은 key에 없습니다.')
        elif menu_num==5:
            continent_name = input('대륙 이름을 입력하세요(Asia, Europe, America): ')
            total_population = 0
            for city, info in contry_list.items():
                if info[1] == continent_name:
                    print(f'{city}: {info[2]:,}')
                    total_population += info[2]
            print(f'{continent_name} 전체 인구수: {total_population:,}')
        elif menu_num==6:
            print('프로그램을 종료합니다.')
            break
main()