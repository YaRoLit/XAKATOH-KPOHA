import datetime as dt

def render_eventlist(df) -> list:
    result_text = []
    row_count = df.shape[0]
        
    for i in range(row_count):
        start_datetime = df.datetime[i].strftime("%d/%m/%Y, %H:%M")
        end_datetime = (df.datetime[i] + dt.timedelta(minutes=int(df.long[i]))).strftime("%H:%M")    
        
        result_text.append(f'{df.event_type[i]}:\n\t{start_datetime} - {end_datetime}, {df.place[i]}')