import imageio
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import cv2
import gc
import matplotlib



def img_file_to_gif(img_files, output_file_name, dur):
    if not os.path.exists("../Vaccin/PlotFile/GIF/"):
        os.makedirs("../Vaccin/PlotFile/GIF/")
    imgs_array = [np.array(cv2.imread(img_file)) for img_file in img_file_lst]
    imageio.mimsave(output_file_name, imgs_array, duration=dur)
    for img_file in img_file_lst:
        os.remove(img_file)
        print("Deleting " + img_file + "...\n")
    print("Finished.\n")



option = int(input("생성할 파일 옵션\n"
    "1.By_Times_Immune: 면역 생성자 변화(animated)\n"
    "2.By_Times_Infect_Rate: 시행별 감염률(image)\n"
    "3.By_Times_Infection: 감염자 변화(animated)\n"
    "4.Immune_Accu: 누적 면역자(image)\n"
    "5.Infection_Accu: 누적 감염자(image)\n"
    "6.Static Tool\n"
    "Option(num): "))

filename_option = None

if option == 1:
    filename_option = "By_Times_Immune"
elif option == 2:
    filename_option = "By_Times_Infect_Rate"
elif option == 3:
    filename_option = "By_Times_Infection"
elif option == 4:
    filename_option = "Immune_Accu"
elif option == 5:
    filename_option = "Infection_Accu"

Vaccin_Rate = int(input("접종률을 입력하세요(0<=n<=100): "))

Setting_file = "/Users/choidaehyun/Documents/GitHub/Vaccin/CalResult/Preference-"+repr(Vaccin_Rate)+".txt"

Preference = np.loadtxt(
            Setting_file,
            delimiter=',',
            dtype='int'
        )
filename = None
COL = Preference[0]
picture_name = None
gif_name = None

Times = Preference[1]
maxval = Preference[2]

Day_File = "/Users/choidaehyun/Documents/GitHub/Vaccin/CalResult/DayList-"+repr(Vaccin_Rate)+".txt"
DayendData = np.loadtxt(
    Day_File,
    delimiter=' ',
    dtype='int'
)

Days = []
if option == 1 or option == 3:


    dur = float(input("재생속도를 입력하세요(default:0.5): "))
    skip = list(map(int, input("건너뛸 시행을 입력하세요: ").split()))

    comeout = 0
    for i in range(Times):
        for k in skip:
            if skip[k-1]-1 == i:
                comeout = 1
                break
        if comeout == 1:
            comeout = 0
            continue


        Days = DayendData[i]
        img_file_lst = []
        for j in range(Days):
            filename = \
                "/Users/choidaehyun/Documents/GitHub/Vaccin/CalResult/" + filename_option + "-" + repr(
                    Vaccin_Rate) + "-" + repr(i + 1) + "-" + repr(j + 1) + ".txt"
            # 종류 접종률 시행 일자
            data = []
            data = np.loadtxt(
                filename,
                delimiter=',',
                dtype='int'
            )
            # print(data)
            print("시행"+repr(i+1)+"/"+repr(round(j/Days*100,2))+"%완료\n")

            if j <= maxval / 6:
                sns.heatmap(data, vmin=0, vmax=1).set(title="Day"+repr(j+1)+" Non Vaccinated")
            else:
                sns.heatmap(data, vmin=0, vmax=1).set(title="Day"+repr(j+1)+" Vaccinated")
            del data
            if option == 1:
                picture_name = "../Vaccin/PlotFile/By_Times_Immune_"+repr(Vaccin_Rate).zfill(3)+"_"+repr(i+1)+"_"+repr(j+1).zfill(4)
            elif option == 3:
                picture_name = "../Vaccin/PlotFile/By_Times_Infection_"+repr(Vaccin_Rate).zfill(3)+"_"+repr(i+1)+"_"+repr(j+1).zfill(4)
          # FileName_Time_Day
            plt.savefig(picture_name)
            img_file_lst.append(picture_name+".png")
            plt.close('all')
            gc.collect()
            matplotlib.use('agg')



        if option == 1:
            gif_name = "../Vaccin/PlotFile/GIF/By_Times_Immune_"+repr(Vaccin_Rate).zfill(3)+"_"+repr(i+1)+".gif"
        elif option == 3:
            gif_name = "../Vaccin/PlotFile/GIF/By_Times_Infection_"+repr(Vaccin_Rate).zfill(3)+"_"+repr(i+1)+".gif"
        img_file_to_gif(img_file_lst,gif_name,dur)
        img_file_lst.clear()


elif option == 2 or option == 4 or option == 5:

    for i in range(Times):
        filename = \
            "/Users/choidaehyun/Documents/GitHub/Vaccin/CalResult/" + filename_option + "-" + repr(
                Vaccin_Rate) + "-" + repr(i + 1) + ".txt"
        data = []
        if option == 2:
            data = np.loadtxt(
                filename,
                delimiter=',',
                dtype='float'
            )
        elif option == 4 or option == 5:
            data = np.loadtxt(
                filename,
                delimiter=',',
                dtype='int'
            )
        if option == 2:
            picture_name = "../Vaccin/PlotFile/By_Times_Infect_Rate_"
        elif option == 4:
            picture_name = "../Vaccin/PlotFile/Immune_Accu_"
        elif option == 5:
            picture_name = "../Vaccin/PlotFile/Infection_Accu_"
        sns.heatmap(data)
        # Filename_Time
        plt.savefig(picture_name + repr(Vaccin_Rate).zfill(3)+"_"+ repr(i + 1))
        plt.close('all')
        plt.clf()
        del data


elif option == 6:
    static_option = int(input("1.Scatter\n"
                              "2.Liner\n"
                              "Option(num): "))
    if static_option == 1:
        Scatter_Option = int(input("1.감염률-"))
    elif static_option == 2:
        Liner_Option = int(input("1. 일별 감염자수 전체\n"
                                 "Option(num): "))
        if Liner_Option == 1:
            for i in range(Times):
                filename = "/Users/choidaehyun/Documents/GitHub/Vaccin/CalResult/" + "By_Day_Infection" + "-" + repr(
                        Vaccin_Rate) + "-" + repr(i + 1) + ".txt"
                data = []
                data = np.loadtxt(
                    filename,
                    delimiter=',',
                    dtype='int'
                )
                by_day_break = []
                by_day_nonvaccin = []
                by_day_all = []
                for j in range(Days):
                    print("시행" + repr(i + 1) + "/" + repr(round(j / Days * 100, 2)) + "%완료\n")
                    by_day_all.append(data[j][0])
                    by_day_nonvaccin.append(data[j][1])
                    by_day_break.append(data[j][2])



                x = range(Days)
                plt.plot(x, by_day_all, xlim=maxval)
                plt.plot(x, by_day_nonvaccin,xlim=maxval)
                plt.plot(x, by_day_break,xlim=maxval)
                picture_name = "../Vaccin/PlotFile/By_Day_Infection_" + repr(Vaccin_Rate).zfill(3) + "_" + repr(
                    i + 1)
                plt.legend(["ALL", "NonVaccin", "Breakthrough"])
                plt.savefig(picture_name)
                img_file_lst.append(picture_name + ".png")
                plt.close('all')
                plt.clf()
                # plt.show()
