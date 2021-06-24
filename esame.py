class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name

    def get_data(self):

        #lista vuota dove salvare i valori(lista di liste)
        values = []

        # provo ad aprire il file
        try:
            my_file = open(self.name, 'r')
        except:
            raise ExamException('il file non esiste o non è leggibile')

        
        for line in my_file:

            #faccio lo split di ogni riga sulla virgola
            elements = line.split(',')

            #se non sto processando l'intestazione
            if elements[0]!='epoch':
                
                #setto epoch e temperatura
                epoch = elements[0]
                temperature = elements[1]

                values.append([int(float(epoch)), float(temperature)])

        #controllo che la lista sia ordinata e che non ci siano timestamp duplicati
        for i in range (0,len(values)-1):
            if values[i][0] >= values[i + 1][0]:
                raise ExamException('la lista non è ordinata')

        for j in range (i+1,len(values)):
            if values[j][0] == values[i][0]:
                raise ExamException('timestamp duplicato')

        my_file.close()
        return values



#creo la funzione compute_daily_variance
def compute_daily_variance(time_series):


    values = [] #lista di liste vuota in cui salvare le temperature giorno per giorno

    for i in range(0,len(time_series)):
        epoch = time_series[i][0]
        day_start_epoch = epoch - (epoch % 86400) #inizio del giorno
        daily_temperatures = [] #lista vuota in cui salvare le temperature di un singolo giorno
        if epoch!=0:
            for j in range(i,len(time_series)):
                timestamp = time_series[j][0]
                day_end_epoch = day_start_epoch + 86400 #fine del giorno
                if timestamp < day_end_epoch: #se sono nello stesso giorno aggiungo le temperature alla lista
                    daily_temperatures.append(time_series[j][1])
                    time_series[j][0]= 0 #assegno il valore 0 alle date così da poterle ignorare in seguito

            values.append(daily_temperatures)
    

    result = [] #lista vuota dove salvare tutte le varianze
    for i in range (0,len(values)): #temperature di tutti i giorni
        if len(values[i])==1: 
            variance = None #la varianza di un solo elemento non è definita
        
        else:
            sum = 0
            for item in values[i]: #dati di un singolo giorno
                sum += item
            mean=sum/len(values[i])
        
            sum_deviations = 0
            for item in values[i]:
                sum_deviations += (item-mean)**2
            variance = sum_deviations/(len(values[i])-1)

        result.append(variance)
    

    return result



time_series_file = CSVTimeSeriesFile(name='data.csv')

time_series = time_series_file.get_data()

print(compute_daily_variance(time_series))