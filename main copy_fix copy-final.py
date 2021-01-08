from os import system 
from time import sleep
import keyboard
from copy import deepcopy
import random

JD_STOP = 0; JD_UP = 1; JD_DOWN = 2
MAP_MAX_X = 50; MAP_MAX_Y = 10
JUMP_MAX = 3
RENDER_BLOCK_Y = 6; RENDER_BLOCK_X = 15
MD_R = 0; MD_L = 1
MONSTER_MAX = 3

class monster:
    def __init__(self, y, x):
        self.movingSpeed = 1.5
        self.movingCount = 0
        self.moveDir = MD_R
        self.pos = [y, x]


class Character:
    def __init__(self, y, x):
        self.pos = [y, x]       # 플레이어의 현재 위치. 0은 y축, 1은 x축
        self.isJump = False     # 플레이어가 지금 점프중인지 나타냄
        self.jumpState = 0      # 플레이어가 점프해서 지금 몇 칸 위로 갔는가?
        self.jumpDir = JD_STOP  # 플레이어의 점프 방향은 어느 쪽인가?
        self.score = 0          # 플레이어의 점수
        self.isComplete = False # 플레이어가 도착점에 도달했는가?
        self.isDead = False     # 플레이어가 죽었는가?
              
              

class Stage:            
    def printMap(self):
        # 맵과 캐릭터를 렌더링한다
        # 아래의 C++ 코드를 참고하여 렌더링 방식을 스크롤 형식으로 변경해야 한다.
        # //맵은 스크롤 처리를 해야한다. 그렇기 때문에 현재
	    # //플레이어가 이동한 위치로부터 맵을 출력해주어야 한다.
	    # //출력 크기는 4 x 10. 지금은 플레이어가 처음에 있다고
	    # //가정하고 처음 4 x 10 출력.
	    # //0:벽	1:길	2:시작점	3:도착점	4:코인

	    # CPlayer* pPlayer = CObjectManager::GetInst()->GetPlayer();

	    # //플레이어의 x, y 좌표를 얻어온다.
	    # int iX = pPlayer->GetX();
	    # int iY = pPlayer->GetY();
        PlayerPos = self.CCharacter.pos
        iY = PlayerPos[0]
        iX = PlayerPos[1]

	    # //맵의 출력은 플레이어의 위치를 중심으로 출력한다.
	    # //세로는 플레이어 2칸 위부터 한 칸 아래까지 출력한다.
	    # //총 4줄이 출력되는 것이다.
	    # //가로는 플레이어 위치부터 오른쪽 10칸까지 출력한다.
	    # //출력될 블럭 수를 2로 나누어주어서 출력될 가장 아래쪽 인덱스를
	    # // 구해준다. 플레이어 위치보다 2칸 아래까지 출력해야 하기 때문이다.
	    # int iYCount = iY + (RENDER_BLOCK_Y / 2);

        iYCount =  iY + (RENDER_BLOCK_Y / 2)

	    # //만약 출력될 아래 2칸이 맵의 가장 아래쪽 개수보다 크거나 같다면
	    # //출력될 아래 인덱스를 가장 마지막 인덱스로 제한한다.
	    # if (iYCount >= BLOCK_Y)
	    # 	iYCount = BLOCK_Y - 1;

        if iYCount >= MAP_MAX_Y:
            iYCount = MAP_MAX_Y - 1

	    # //출력해야 할 최소 인덱스를 구해준다.
	    # //출력해야 할 가장 아래쪽 인덱스에서 출력해야할 개수 - 1 개를 빼주게 되면
	    # //출력해야 할 인덱스가 9이고 5개 출력시 9-4가 되므로
	    # //5~9까지의 반복이 돌 수 있도록 최소값을 잡아준다.
	    # int iYMin = iYCount - (RENDER_BLOCK_Y - 1);

        iYMin = iYCount - (RENDER_BLOCK_Y - 1)


	    # //만약 최소값이 0보다 작다면 인덱스가 없으므로 0으로 제한해준다.
	    # if (iYMin < 0)
	    # 	iYMin = 0;
        if iYMin < 0:
            iYMin = 0

	    # //가로줄 최대 출력수는 현재 플레이어 위치 + 출력해야 할 가로개수이다.
	    # int iXCount = iX + RENDER_BLOCK_X;

        iXCount = iX + RENDER_BLOCK_X

	    # //출력해야 할 가로 인덱스 최대치가 전체 블럭 수보다 크다면
	    # //잘못된 인덱스이므로 최대 블럭 수로 제한해준다.
	    # //아래 for문에서 구해준 이 값보다 작을때까지만 돌리기 때문이다.
	    # if (iXCount > BLOCK_X)
	    # 	iXCount = BLOCK_X;
        if iXCount > MAP_MAX_X:
            iXCount = MAP_MAX_X

	    # //X의 최소 인덱스는 플레이어의 최소 위치이다.
	    # int iXMin = iX;
        iXMin = iX

	    # //가장 마지막 길 10칸은 모두 보여주기 위해서 반복문의 최소값을
	    # //블럭 전체 길이 - 출력된 블럭으로 처리해준다.
	    # if (iXMin > BLOCK_X - RENDER_BLOCK_X)
	    # 	iXMin = BLOCK_X - RENDER_BLOCK_X;
        if iXMin > MAP_MAX_X - RENDER_BLOCK_X:
            iXMin = MAP_MAX_X - RENDER_BLOCK_X

	    # for (int i = iYMin; i <= iYCount; ++i)
	    # {
	    # 	for (int j = iXMin; j < iXCount; ++j)
	    # 	{
	    # 		if (i == iY && j == iX)
	    # 			cout << "§";
	    # 		else if (m_cStage[i][j] == SBT_WALL)
	    # 			cout << "■";
	    # 		else if (m_cStage[i][j] == SBT_ROAD)
	    # 			cout << "  ";
	    # 		else if (m_cStage[i][j] == SBT_START)
	    # 			cout << "◑";
	    # 		else if (m_cStage[i][j] == SBT_END)
	    # 			cout << "◐";
	    # 		else if (m_cStage[i][j] == SBT_COIN)
	    # 			cout << "@";
	    # 		else if (m_cStage[i][j] == SBT_ITEM_BULLET)
	    # 			cout << "♥";
	    # 		else if (m_cStage[i][j] == SBT_ITEM_BIG)
	    # 			cout << "◎";
	    # 	}
	    # 	cout << endl;
	    # }
        
        for y in range(int(iYMin), int(iYCount)):
                for x in range(int(iXMin), int(iXCount)):  
                    if (y == self.monsterList[0].pos[0] and x == self.monsterList[0].pos[1]) or (y == self.monsterList[1].pos[0] and x == self.monsterList[1].pos[1]) or (y == self.monsterList[2].pos[0] and x == self.monsterList[2].pos[1]):
                        print('\033[32m'+'ꇹ'+'\033[0m', end='')
                    elif y == self.CCharacter.pos[0] and x == self.CCharacter.pos[1] and not self.CCharacter.isJump:
                        # 만약 지금 출력하고자 하는 위치에 플레이어가 위치한다면
                        # map의 해당 위치에 있는 블록 대신 플레이어를 출력한다.
                        print('\033[31m'+'ꆜ'+'\033[0m', end='')
                    elif y == self.CCharacter.pos[0] and x == self.CCharacter.pos[1] and self.CCharacter.isJump:
                        # 만약 지금 출력하고자 하는 위치에 플레이어가 위치한다면
                        # map의 해당 위치에 있는 블록 대신 플레이어를 출력한다.
                        print('\033[31m'+'ꂿ'+'\033[0m', end='')
                    elif self.map[y][x] == "0":
                        print('  ', end='')
                    elif self.map[y][x] == "1":
                        print('■■', end='')
                    elif self.map[y][x] == "2":
                        print('\033[34m'+'◐'+'\033[0m', end='')
                    elif self.map[y][x] == "3":
                        print('\033[34m'+'◑'+'\033[0m', end='')
                    elif self.map[y][x] == '4':
                        print('\033[33m'+'ⓒ '+'\033[0m', end='')
                # 한 줄 출력이 끝났으면 개행한다.
                print()
    

    # # 구현 필요 : 플레이어의 입력에 맞춰 Charater의 pos를 변화시키고 상태를 업데이트합니다.
    # # 파이썬에서 가능할지 모르겠지만, win32 API의 GetAsyncKeyState 함수를 사용하면
    # # 구현할 수 있을 것 같습니다. 꼭 그것이 아니더라도 플레이어의 입력을
    # # 대기 없이 즉시 인식하는 함수를 쓰면 될 것 같습니다.
    def updatePos(self):
        playerPos = self.CCharacter.pos
        
        if keyboard.is_pressed('a'):
            if playerPos[1] > 0:
                if self.map[playerPos[0]][playerPos[1]-1] != '1':
                    self.CCharacter.pos[1] -= 1
    
        elif keyboard.is_pressed('d'):
            if playerPos[1] < MAP_MAX_X:
                if self.map[playerPos[0]][playerPos[1]+1] != '1':
                    self.CCharacter.pos[1] += 1
                
        if keyboard.is_pressed('space'): # 아무 키를 입력받으면 isJump를 True로 바꾸며 jumpDir을 JU_UP으로 바꿉니다.
            if not self.CCharacter.isJump:
                self.CCharacter.isJump = True
                self.CCharacter.jumpDir = JD_UP
                self.CCharacter.jumpState = 0


        if self.CCharacter.isJump == True:
            # 점프 방향이 위쪽인 경우 
            if(self.CCharacter.jumpDir == JD_UP):
                self.CCharacter.jumpState += 1     # jumpState를 1 증가시킵니다.
                if self.CCharacter.jumpState > JUMP_MAX:
                    # jumpState를 JUMP_MAX로 맞추고 jumpDir을 아래로 바꿉니다.
                    self.CCharacter.jumpState = JUMP_MAX
                    self.CCharacter.jumpDir = JD_DOWN
                elif self.map[playerPos[0]-1][playerPos[1]] == '1' : #지금 플레이어 머리 위에 블록이 있는 경우
                    self.CCharacter.jumpState -= 1    # jumpState를 1 감소시킵니다.
                    self.CCharacter.jumpDir = JD_DOWN # jumpDir을 아래로 바꿉니다.
                else:
                     # 플레이어의 위치를 y축 위로 1 이동시킵니다.
                    self.CCharacter.pos[0] -= 1
            elif (self.CCharacter.jumpDir == JD_DOWN):
                if (playerPos[0] >= MAP_MAX_Y) :# 플레이어의 y축 위치가 MAP_MAX_Y보다 아래 있을 경우 플레이어는 사망합니다.
                    self.CCharacter.isDead = True # 그 경우 isDead = True가 됩니다.
                elif self.map[playerPos[0]+1][playerPos[1]] =='1': # 플레이어의 발 아래 블록이 있는 경우 jumpDir을 JD_STOP으로 바꾸고
                     self.CCharacter.jumDir = JD_STOP
                     self.CCharacter.isJump = False #isJump를 False로 바꿉니다.
                else:
                    self.CCharacter.pos[0] += 1 # 위의 두 조건이 모두 아닐 경우 플레이어를 y축 아래로 1 이동시킵니다.

        # 점프를 하지 않을 상태일때 발 아래가 공백인지 검사합니다.
        try:
            if ((self.map[playerPos[0]+1][playerPos[1]] !='1') and not self.CCharacter.isJump): # 발 아래 블록이 공백이며 동시에 점프 상태가 아닐 경우
                self.CCharacter.pos[0] += 1  #플레이어를 y축 아래로 1 이동시킵니다.
        except:
            self.CCharacter.isDead = True
       
        # 만약 플레이어의 현 위치에 코인이 있을 경우 코인을 먹습니다.
        if(self.map[playerPos[0]][playerPos[1]] =='4') : # 플레이어의 현 위치에 코인이 있을 경우
            self.CCharacter.score += 1000   # score를 1000 증가시킵니다
            # 현 위치의 map의 코인을 공백으로 변경합니다.
            self.map[playerPos[0]][playerPos[1]] = '0'
    
        # 만약 플레이어의 현 위치가 도착점인 경우 isComplete가 True가 됩니다.
        if(self.map[playerPos[0]][playerPos[1]] == '3'):
            self.CCharacter.isComplete = True
    
        #플레이어가 죽었을 경우
        if (self.CCharacter.isDead == True):
            self.CCharacter.isDead = False
            # 플레이어 사망 메세지 출력
            print("저런... 죽으셨어요...ㅠ")
            # 코인 점수 + 포지션 점수 \n 최종 점수
            print(f"코인 점수: {self.CCharacter.score}점    거리 점수: {playerPos[1]* 100}점")
            print(f"누적 점수: {self.storedScore}점\n")
            print(f"최종 점수 : {self.CCharacter.score + playerPos[1]* 100 + self.storedScore}점")
            # 점수 초기화
            self.CCharacter.score = 0
            # 누적 점수 초기화
            self.storedScore = 0
            # map을 변경되기 전 초기 상태로 되돌립니다.
            self.map = deepcopy(self.mapO)
            # 플레이어의 위치를 startPos로 변경합니다.
            self.CCharacter.pos = deepcopy(self.startPos)
            system('pause')   # 일시 정지합니다
            # return
    
    def updateMonsterPos(self):
        for m in self.monsterList:
            m.movingCount += 1
            if(m.movingCount > m.movingSpeed):
                if(m.moveDir == MD_R):
                    m.movingCount = 0
                    if(self.map[m.pos[0]+1][m.pos[1]+1] == '1'):
                        m.pos[1] += 1
                    else:
                        m.moveDir=MD_L
                else:
                    m.movingCount = 0
                    if(self.map[m.pos[0]+1][m.pos[1]-1] == '1'):
                        m.pos[1] -= 1
                    else:
                        m.moveDir=MD_R
            if(m.pos[0] == self.CCharacter.pos[0] and m.pos[1] == self.CCharacter.pos[1]):
                self.CCharacter.score -= 1000
            
    def __init__(self, mapT, score):
        # map을 변경 가능한 list의 형태로 바꿉니다.
        self.storedScore = score
        self.map = list(mapT)
        self.mapO = []
        for i in range(MAP_MAX_Y):
            self.map[i] = list(self.map[i])
        self.mapO = deepcopy(self.map)
        # 게임이 시작되기 전에 map에서 시작점의 위치를 찾아서 Character의 현재 위치로 설정해준다.
        for y in range(MAP_MAX_Y):
            for x in range(MAP_MAX_X):
                if self.map[y][x] == "2":
                    self.startPos = [y, x]
                    self.CCharacter = Character(self.startPos[0], self.startPos[1])
                    break
        # 몬스터를 스폰하기 위해 스폰 가능한 블록의 리스트를 생성한다.
        self.blockList = []
        # 몬스터의 리스트를 생성한다
        self.monsterList = []
        for y in range(MAP_MAX_Y):
            for x in range(7, MAP_MAX_X-7):
                if self.map[y][x] == "1":
                    self.blockList.append([y, x])
        random.shuffle(self.blockList)
        for i in range(MONSTER_MAX):
            self.monsterList.append(monster(self.blockList[i][0]-1, self.blockList[i][1]))

    def runGame(self):
        # 플레이어가 도착점에 도달할 때까지 아래의 반복문을 반복한다.
        while(self.CCharacter.isComplete == False):
            # 기존 화면을 비워준다.
            system('cls')
            self.printMap()  # 맵을 랜더링한다
            self.updatePos()            # 플레이어의 위치를 변경한다.
            self.updateMonsterPos()
            print(f"코인 점수: {self.CCharacter.score}점    거리 점수: {self.CCharacter.pos[1]* 100}점")
            print(f"누적 점수: {self.storedScore}점\n")
            print("a : 왼쪽     d : 오른쪽      space : 점프")
            # 만약 플레이어가 도착점에 도달했을 경우 완료 메세지를 출력하고 break합니다.

            # 반복문을 다시 실행하기 전 잠시 대기한다.
            sleep(0.1)
        # 플레이어가 도착하면 완료 메세지를 띄워준다
        # 코인 점수 + 포지션 점수 \n 최종 점수
        print("축하합니다! 짱짱!")
        print(f"최종 점수 : {self.CCharacter.score + self.CCharacter.pos[1] * 100 + self.storedScore}점")
        returnScore = self.CCharacter.score + self.CCharacter.pos[1] * 100 + self.storedScore
        # 점수 초기화
        self.CCharacter.score = 0
        # map을 변경되기 전 초기 상태로 되돌립니다.
        self.map = self.mapO
        # 플레이어의 위치를 startPos로 변경합니다.
        self.CCharacter.pos = self.startPos
        system('pause')   # 일시 정지합니다
        return returnScore


class MapManager:
    def __init__(self):
        # 50 X 10
        # 0: 공백
        # 1: 블록
        # 2: 시작점
        # 3: 도착점
        # 4: 코인
        #
        # 맵들의 원본 리스트이다. 게임 내에서 변경 불가능하다.
        # 이 맵들은 Stage 클래스 객체로 복사된 뒤, 출력되고 변경된다.
        self.mapTuple=((  
            "00000000000000000000000000000000000000000000000000",
            "00000000000000000000000000000000000000000000000000",
            "00000000000000000000000000004400000044000000000000",
            "00000000000000000000000000000000000000000000000000",
            "00000000000000000000000011100001111000000000000000",
            "00000000000000000000000000000000000000440000000000",
            "00000000044000004400111044000044000000000000000000",
            "20000000000000000000000000000000000001111000000003",
            "11111111100111110011111100111100111000000001111111",
            "00000000000000000000000000000000000000000000000000"
        ),
        (  
            "00000000000000000000000000000000000000000000000000",
            "00000000000000000000000000000000000000000000000000",
            "00000000000000000000000000004400000044000000000000",
            "00000000000000000000000000000000000000000000000000",
            "00000000000000110000000011100001111000000000000000",
            "00000000000000000000000000000000000000440000000000",
            "00000000011000004400111044000044000000000000000000",
            "20001100000000000000000000000000000001111000000003",
            "11111111100111110011111100111100111000000001111111",
            "00000000000000000000000000000000000000000000000000"
        ) )

    def runGame(self, stage, score):
        CStage = Stage(self.mapTuple[stage-1], score)
        returnScore = CStage.runGame()
        return returnScore


# 매인 메뉴를 담당하는 클래스이다. 
class Core:
    def printMain(self):
        print("1. Stage1")
        print("2. Stage2")
        print("3. Exit")
        stage = int(input("스테이지를 선택하세요 : "))

        return stage
    
    def runGame(self, stage, score):
        if(stage == 3):
            return
        else:
            CMapManager = MapManager()
            returnScore = CMapManager.runGame(stage, score)
            return returnScore


def init():
    CCore = Core()
    score = 0
    while True:
        system('cls')
        inputStage = CCore.printMain()
        while True:
            if(inputStage==3):
                print("게임을 종료합니다.")
                return
            else:
                score = CCore.runGame(inputStage, score)    #CCore에서 스테이지를 선택한 후 게임을 실행한다.
            inputStage += 1

init()