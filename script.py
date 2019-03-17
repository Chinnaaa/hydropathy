import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import xlwt 
from xlwt import Workbook 

class hydrophobicity:
    def get_plot(user_input,windoww):
        # user_input = input("Type your amino acid sequence: ")
        # windoww = input("window size: ")
        window = int(windoww)
        user_input = user_input.upper()
        #user_input= ''.join(user_input.split())
        length = len(user_input)
        arrayy = []
        normalize=[]
        scores = {'G':0.00,'C':1.15,'I':0.97,'L':0.87,'F':0.85,'V':0.83,'W':0.67,'Y':0.60,'M':0.54,'A':0.33,'P':0.32,'H':0.25,'T':0.21,'S':0.05,'R':-0.01,'Q':-0.05,'N':-0.07,'D':-0.22,'E':-0.24,'K':-0.40}
        name = {'A':"Ala",'R':"Arg",'N':"Asn",'D':"Asp",'C':"Cys",'E':"Glu",'Q':"Gln",'G':"Gly",'H':"His",'I':"Ile",'L':"Leu",'K':"Lys",'M':"Met",'F':"Phe",'P':"Pro",'S':"Ser",'T':"Thr",'W':"Trp",'Y':"Tyr",'V':"Val"}

        for x in user_input:
            normalize.append(scores[x])

        for index in range(0,len(normalize)-window+1):
            summm=0
            for i in range(window):
                summm+=normalize[index+i]

            arrayy.append(summm/window)




        yaxis=[]
        count = 0
        summ = 0

        for x in arrayy:
            summ = x+summ
            count=count+1
            if count%window==0:
                yaxis.append(summ/window)
                summ=0

        print ("Length of amino acid sequence: %d" %(length))
        print ("Window Size: %d" %(window))

        y_axis= np.array(yaxis)
        length = len(arrayy) - len(arrayy)%window
        t = np.arange(int(window/2), length, window)
        x_axis=np.array(t)
        print ("Number of points plotted: %d" %(len(x_axis)))
        fig, ax = plt.subplots()
        ax.plot(x_axis, y_axis)
        ax.set(xlabel='Amino acid sequence position', ylabel='Hydrophobicity score',
               title='''  Bandyopadhyay-Mehler Hydropathy plot  ''')

        ax.grid()
        fig.savefig("static/pdfs/Hydropathy_Plot.pdf")
        
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        
        wb = Workbook() 
        sheet1 = wb.add_sheet('Sheet 1') 
        sheet1.write(0,0,"Position")
        sheet1.write(0,1,"Amino acid")
        sheet1.write(0,2,"Hydrophobicity Score")

        for i in range(len(arrayy)):
            sheet1.write(i+1,2,arrayy[i])
            sheet1.write(i+1,0,i+(window/2)-0.5+1)
            sheet1.write(i+1,1,name[user_input[int(i+(window/2)-0.5)]])

        wb.save('static/pdfs/Hydrophobicity_scores.xls')

        return 'data:image/png;base64,{}'.format(graph_url)

"""if __name__=="__main__":
    h = hydrophobicity()
    h.get_plot()
"""
