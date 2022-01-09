def Show_Emotiv_State(VAL, ENG, FOC, EXC, MED, FRU):
        try:
            print("Engagement(ENG) : %.2f" % ENG, end=" ")
            print("Excitement(EXC) : %.2f" % EXC, end=" ")
            print('Focus(FOC) : %.2f' % FOC, end=" ")
            print('Interest(VAL) : %.2f' % VAL, end=" ")
            print('Relaxtion(MED) : %.2f' % MED, end=" ")
            print('Stress(FUR) : %.2f' % FRU)
        except:
            print("Null")