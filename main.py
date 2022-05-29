def solution(minterm):
    answer = []
    answer2 = []
    final = []
    for i in range(2, len(minterm)):
        k = format(minterm[i], 'b')
        if (len(k) < minterm[0]):
            k = str(k).zfill(minterm[0])
            answer2.append(k)
        elif (len(k) == minterm[0]):
            answer2.append(k)
    for i in range(0, minterm[0] + 1):
        myarray = []
        for j in answer2:
            cnt = 0
            for k in range(0, len(j)):
                if (j[k] == "1"):
                    cnt = cnt + 1
                else:
                    continue
            if (cnt == i):
                myarray.append(j)
        answer.append(myarray)
    length = len(answer)
    pi_result, checkpi = combine(answer, minterm[0] + 1)
    while (length != 0):
        pi_result, checkpi = combine(pi_result, minterm[0] + 1)
        for i in range(0, len(checkpi)):
            final.append(checkpi[i])
        length = length - 1

    for i in range(0, len(final)):
        a = final[i].replace('-', '2')
        final[i] = a
    final.sort()
    for i in range(0, len(final)):
        a = final[i].replace('2', '-')
        final[i] = a

    print("start pi's ",final,"minterms",answer2)
    print("----------------------------------------------------------------------------------------------------------------")
    print("EPI Checking and Using EPI to remove ")
    final2 = [] ## EPi를 담을 리스트
    minlist =[] ## minterm들을 담을 리스트
    for i in answer2:
        minlist.append(i) # answer2는 민텀을 이진수로 바꾼 것들을 넣어둔 배열 -> 그대로 minlist에 넣어줌

    for i in answer2:
        epi = []
        mt = i
        for j in final: #final은 그냥 pi들을 담은 리스트 final2는 epi를 담은 리스트
            s = ""
            for l in range(len(i)):
                if j[l] == '-':
                    s += i[l]
                else:
                    s += j[l]
            if i == s: # 한글자씩 비교하여 빈 스트링에 넣어주고 '-'는 민텀의 그 자리 숫자로 바꾸어줌
                epi.append(j) # 같으면 포함되는 것 (체크) 이므로 epi라는 배열에 넣어줌

        if len(epi) == 1:  #이진수 민텀하나와 pi들을 차례로 하나씩 다 비교한 후 epi배열을 봤을때 길이가 1이면 담당하는 pi가 하나라는 것, 즉 epi
            if epi[0] not in final2: #중복을 제거하기 위한 코드
                final2.append(epi[0])
        for k in range(0,len(final2)):
            if final2[k] in epi :
                if mt in minlist : #epi를 확인하는 배열에서 epi를 가지고있다면 그 때의 민텀들도 싹다 지워줌
                    minlist.remove(mt)
                    print("Because of first EPI", "'" + final2[k] + "'", "====>", "Minterm", "'" + mt + "'","is removed ")

    for i in final2:
        if i in final : #epi들을 pi리스트에서 다 제거해줌
            final.remove(i)
            print("fisrt EPI ", "'" + i + "'", "is removed")
    coverlist = [] # first epi 뿐만 아니라 그 후에 나올 epi들을 모두 모아줄 final coverlist
    coverlist = coverlist + final2 # final2 는 첫번째 epi가 담긴 리스트 . cover에 포함시켜줌

    ##여기까지 첫번째 epi가 포함한 로우컬럼 모두 지우고 시작
    print("first epi =>", final2,"   ","covering minterm, PI's => ",coverlist ) ##first epi
    print("After removed first epi, PIlist=>", final, "After remove first epi ,mintermlist=>", minlist,"\n") #first epi로 다 지운후의 pi와 minterms


    while (True) : # cd , rd , find epi , cd ,rd ... 순서대로 계속 반복해야 하므로 카운트가 정해져있지 않아서 와일문을 사용해봄

        #Colum dominance
        colchecklist = [[] for i in range(100)] #minterm 별로 체크된 pi들을 모아주기 위한 리스트를 만듬
        cnt = 0
        for i in minlist :
            a = colcheck(i,final) #함수호출 체크된 PI들을 민텀별로 모아줌 칼럼별로 비교하기위함 .
            colchecklist[cnt].append(a) # 순차적으로 pi들을 넣어주었음
            cnt = cnt+1
        colchecklist = sum(colchecklist,[]) #1차원 배열로 합쳐줌 .

        colrmlist =[] # 지우기위한 리스트를 만듬 remove사용시 인덱스가 꼬여서 마지막에 리스트에 포함된 것들만 지워주기 위함 .
        print("Before CD ,PIlist=>", final, "Before CD, mintermlist=>", minlist)
        for i in range(0, len(colchecklist)):
            for j in range(0,len(colchecklist)):
                if len(colchecklist[i]) == len(colchecklist[j]):  ## 원소개수가 같으면 지배관계가 안나타남 .
                    if i == j: ## 자신이 자신을 검사할때 그냥 넘겨줌
                        continue
                    elif i < j: # 왼쪽에서 오른쪽으로만 검사하면 모든경우 검사가능
                        cnt = 0
                        for k in colchecklist[i]:
                            for p in colchecklist[j]:
                                if k == p:
                                    cnt += 1
                        if cnt == len(colchecklist[j]):  ##interchangable
                            if final[j] not in colchecklist: #interchangable중 하나만 고르기 위하여 .
                                print("removed interchangable col", "'" + final[i] + "'", ">-->", "'" + final[j] + "'")
                                rowrmlist.append(final[j]) #뒤에꺼를 임의로 골라줌
                elif len(colchecklist[i]) > len(colchecklist[j]):  ## 앞의 체크리스트가 뒤 체크리스트를 지배할 수 있는 경우
                    cnt= 0 #체크하는 pi가 일치하는 개수
                    for k in colchecklist[i]:
                        for p in colchecklist[j]:
                            if (k == p): #체크하는 pi가 같으면
                                cnt = cnt + 1
                    if len(colchecklist[j]) == cnt : ##체크하는 pi개수가 더 적은 체크리스트 길이와 같으면 포함관계.
                        print("col dominance occured","'"+minlist[i]+"'", ">-->", "'"+minlist[j]+"'")
                        colrmlist.append(minlist[i]) ## checklist[i]의 민텀이 지워져야하므로 i번째가 minlist의 민텀이다.

        for i in colrmlist:
            if i in minlist :
                minlist.remove(i) #cd 후 민텀자체를 세로로 다 지워줘야함.


        print("After CD ,PIlist=>", final, "After CD, mintermlist=>", minlist,"\n")


        #ROW dominance
        print("Before RD, PIlist=>", final, "Before RD , mintermlist=>", minlist)
        rowchecklist = [[] for i in range(100)]
        cnt2 = 0
        for i in final :  # col dominance와 똑같은 방식으로 구현됨 . 함수호출을 하지않아서 변수이름이 조금씩 상이함 .
            b = rowcheck(i,minlist)
            rowchecklist[cnt2].append(b)
            cnt2 =cnt2 +1
        rowchecklist = sum(rowchecklist, [])
        rowrmlist = []
        for i in range(0,len(rowchecklist)):
            for j in range(0,len(rowchecklist)):
                if(len(rowchecklist[i]) == len(rowchecklist[j])): ##지배관계가 안나타날때, interchangable 가능
                    if i ==j :
                        continue
                    elif i< j :
                        cnt = 0
                        for k in rowchecklist[i]:
                            for p in rowchecklist[j]:
                                if k == p:
                                    cnt += 1
                        if cnt == len(rowchecklist[j]):  ##interchangable
                            if final[j] not in rowchecklist:
                                print("removed interchangable row","'"+ final[i]+"'", ">-->", "'"+final[j]+"'")
                                rowrmlist.append(final[j])

                elif (len(rowchecklist[i]) > len(rowchecklist[j])): #더 체크가 많이 된 경우 지배함
                    cnt = 0
                    for k in rowchecklist[i]:
                        for p in rowchecklist[j]:
                            if(k==p):
                                cnt = cnt+1
                    if(len(rowchecklist[j])== cnt):
                        print("row dominance occured","'"+final[i]+"'",">-->","'"+final[j]+"'")
                        rowrmlist.append(final[j]) # 지배 당하는 쪽을 지워야해서 리무브리스트에 넣어줌 바로 지워주면 인덱스에러 발생

        for i in rowrmlist: #해당하는 pi를 제거
            if i in final :
                final.remove(i)


        print("After RD, PIlist=>", final, "After RD , mintermlist=>", minlist,"\n")

        final3 = []
        minlist2 = []

        ##epi를 구해야함 .
        print("checking NEXT EPI .... ")
        print("Before checking EPI, PIlist=>", final, "Before checking EPI , mintermlist=>", minlist)
        for i in minlist : # rd에서 또 다른 변수 사용
            minlist2.append(i)

        for i in minlist:
            epi = []
            mt = i
            for j in final:
                s = ""
                for l in range(len(i)):
                    if j[l] == '-':
                        s += i[l]
                    else:
                        s += j[l]
                if i == s:
                    epi.append(j)

            if len(epi) == 1:
                if epi[0] not in final3:
                    final3.append(epi[0])

            for k in range(0, len(final3)):
                if final3[k] in epi:
                    if mt in minlist2:
                        minlist2.remove(mt)
                        print("Because of first EPI", "'" + final3[k] + "'", "====>", "Minterm", "'" + mt + "'","is removed ")

        for i in minlist:
            epi = []
            mt = i
            for j in final:
                s = ""
                for l in range(len(i)):
                    if j[l] == '-':
                        s += i[l]
                    else:
                        s += j[l]
                if i == s:
                    epi.append(j)

            if len(epi) == 1:
                if epi[0] not in final3:
                    final3.append(epi[0])

            for k in range(0, len(final3)):
                if final3[k] in epi:
                    if mt in minlist2:
                        minlist2.remove(mt)
                        print("Because of first EPI", "'" + final3[k] + "'", "====>", "Minterm", "'" + mt + "'","is removed ")

        # epi가 표에서 늦게(오른쪽) 등장하면 그 전의 민텀들을 지우지 못한다. 그래서 final3에 epi들을 저장시켜놓고 똑같은 포문을 한번
        # 더 돌려주면 왼쪽에 있는 epi를 포함하는 민텀까지 다 지울 수 있다. 비효율적인 방법이긴 하다 .


        for i in final3:
            if i in final:
                final.remove(i)
                print("next EPI ","'"+i+"'", "is removed") # epi에 해당하는 pi 지우기

        if len(final)>0 and len(minlist2) ==0 :# 예외처리 colum을 다 지워줘도 row가 남을때가 생김.
            final.remove(final[0])

        coverlist = coverlist +final3 ## next epi들을 final cover에 포함시켜줌
        print("Next epi= ", final3," covering minterm, PI's", coverlist)
        print("After checking epi ,final=>", final, "After checking epi ,minlist =>", minlist2)

        if(len(final) ==0 and len(minlist2) == 0): ## pilist와 minlist가 다 사라졌으면 끝
            print("FINAL Cover  ==> ", coverlist )
            break

        ## 아직 pi와 MInterm이 남아있다면 계속 와일문을 돌아야함 앞에 minList가 다르므로 다시 minlist를 초기화하고 갱신된 minlist2의 원소를 넣어줌
        if(len(final)>0 and len(minlist2) >0):
            minlist = []
            for i in minlist2 :
                minlist.append(i)
            continue



def combine(answer, length): #pi를 구할때 사용된 이진수 병합 함수이다.
    check = sum(answer, [])
    possible_combine = [[] for i in range(length - 1)]
    for i in range(0, len(answer) - 1):
        for j in answer[i]:
            if (i == len(answer) - 1):
                break
            else:
                for k in answer[i + 1]:
                    s = ""
                    cnt = 0
                    HD = 0
                    for l in range(0, length - 1):
                        if k[l] == j[l]:
                            s = s + k[l]
                            if (k[l] == "1"):
                                cnt = cnt + 1
                        elif k[l] != j[l]:
                            if ((k[l] == '-') or (j[l] == '-')):
                                HD = 0
                                break
                            else:
                                s = s + "-"
                                HD += 1
                                HD_idx = l
                    if (HD == 0):
                        continue
                    if (HD == 1):
                        if s not in possible_combine[cnt]:
                            possible_combine[cnt].append(s)

                        if j in check:
                            check.remove(j)
                        if k in check:
                            check.remove(k)

    answer = possible_combine
    return answer, check


def colcheck(min,final): #각 minterm이 체크하고있는 pi들을 구하기 위한 함수이다 .
    checklist = []
    for j in final:
        s = ""
        for l in range(len(j)):
            if j[l] == '-':
                s += min[l]
            else:
                s += j[l]
        if min == s:
            checklist.append(j)
    return checklist

def rowcheck(final,min ) :
    checklist = []
    for j in min:
        s = ""
        for l in range(len(j)):
            if final[l] == '-':
                s += j[l]
            else:
                s += final[l]
        if j == s:
            checklist.append(j)
    return checklist


solution([4,9,2,3,5,7,8,10,12,13,15])