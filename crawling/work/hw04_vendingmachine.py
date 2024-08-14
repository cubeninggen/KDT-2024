class VendingMachine:
    def __init__(self, input_dict):
        """
        생성자
        :param input_dict: 초기 자판기 재료량(dict 형태)
        """
        self.input_money = 0
        self.inventory = input_dict

    def run(self):
        """
        커피 자판기 동작 및 메뉴 호출 함수
        """
        self.insert_money()
        while True:
            print(f"\n----------------------------------------")
            print(f"\t\t커피 자판기 (잔액:{self.input_money}원)")
            print(f"----------------------------------------")
            print("1. 블랙 커피")
            print("2. 프림 커피")
            print("3. 설탕 프림 커피")
            print("4. 재료 현황")
            print("5. 종료")
            menu = int(input("메뉴를 선택하세요: "))
            
            if menu == 1:
                self.make_coffee("블랙 커피", 30, 0, 0, 100)
            elif menu == 2:
                self.make_coffee("프림 커피", 15, 15, 0, 100)
            elif menu == 3:
                self.make_coffee("설탕 프림 커피", 10, 10, 10, 100)
            elif menu == 4:
                self.show_inventory()
            elif menu == 5:
                self.end_vending()
                break
            else:
                print("잘못된 선택입니다. 다시 선택해주세요.")

    def insert_money(self):
        """
        동전 투입 함수
        """
        self.input_money = int(input("동전을 투입하세요: "))
        if self.input_money < 300:
            print(f"투입된 돈 ({self.input_money}원)이 300원보다 작습니다.")
            print(f"{self.input_money}원을 반환합니다.")
            print("-------------------------------")
            print("커피 자판기 동작을 종료합니다.")
            exit()

    def check_inventory(self, coffee, cream, sugar, water):
        """
        재료가 충분한지 체크하는 함수
        """
        if self.inventory['coffee'] < coffee or \
           self.inventory['cream'] < cream or \
           self.inventory['sugar'] < sugar or \
           self.inventory['water'] < water or \
           self.inventory['cup'] < 1:
            return False
        return True

    def make_coffee(self, coffee_type, coffee, cream, sugar, water):
        """
        커피 제조 함수
        """
        if not self.check_inventory(coffee, cream, sugar, water):
            print("재료가 부족합니다.")
            self.show_inventory()
            print(f"{self.input_money}원을 반환합니다.")
            print("-------------------------------")
            print("커피 자판기 동작을 종료합니다.")
            exit()

        # 재료 소모
        self.inventory['coffee'] -= coffee
        self.inventory['cream'] -= cream
        self.inventory['sugar'] -= sugar
        self.inventory['water'] -= water
        self.inventory['cup'] -= 1
        self.inventory['change'] += 300
        self.input_money -= 300

        print(f"{coffee_type}를 선택하셨습니다. 잔액: {self.input_money}")
        self.show_inventory()

        if self.input_money < 300:
            print(f"잔액이 ({self.input_money}원)이 300원보다 작습니다.")
            print(f"{self.input_money}원을 반환합니다.")
            print("-------------------------------")
            print("커피 자판기 동작을 종료합니다.")
            exit()

    def show_inventory(self):
        """
        현재 재료 현황 출력 함수
        """
        print("------------------------------------------------------------------------------------------")
        print(f"재료 현황: coffee: {self.inventory['coffee']} cream: {self.inventory['cream']} sugar: {self.inventory['sugar']} water: {self.inventory['water']} cup: {self.inventory['cup']} change: {self.inventory['change']}")
        print("------------------------------------------------------------------------------------------")

    def end_vending(self):
        """
        자판기 종료 함수
        """
        print(f"종료를 선택했습니다. {self.input_money}원이 반환됩니다.")
        print("-------------------------------")
        print("커피 자판기 동작을 종료합니다.")


# VendingMachine 객체 생성
inventory_dict = {
    'coffee': 100,
    'cream': 100,
    'sugar': 100,
    'water': 500,
    'cup': 5,
    'change': 0
}
coffee_machine = VendingMachine(inventory_dict)
coffee_machine.run()
