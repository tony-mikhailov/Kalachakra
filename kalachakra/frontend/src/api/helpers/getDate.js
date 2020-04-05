export default function getDateFromURL(params){

    const currentDare = new Date();

    const dateFull={
        year: +params.year || currentDare.getFullYear(),
        month: Math.min(12, params.month || (currentDare.getMonth()+1)),
        day: Math.min(31, params.day || currentDare.getDate()),
    }
     
    dateFull.monthWord = new Date(dateFull.year, dateFull.month - 1, dateFull.day).toLocaleString('ru', {
        month: 'long'
    });

    //Next month
    dateFull.monthNext={
        month: dateFull.month < 12 ? dateFull.month + 1 : 1,
        year: dateFull.month < 12 ? dateFull.year : dateFull.year + 1 
    }

    //Prev month
    dateFull.monthPrev={
        month: dateFull.month > 1 ? dateFull.month - 1 : 12,
        year: dateFull.month > 1 ? dateFull.year : dateFull.year - 1 
    };

    // Next day
    dateFull.dayNext = {
        day: Math.min(31, dateFull.day + 1),
        month: dateFull.month,
        year: dateFull.year
    }

    if (dateFull.month == 4
    || dateFull.month == 6
    || dateFull.month == 9
    || dateFull.month == 11
    ){
        dateFull.dayNext.day = Math.min(30, dateFull.day + 1)
    };
    if (dateFull.month == 2){
        dateFull.dayNext.day = Math.min((dateFull.year % 4) ? 28 : 29, dateFull.day + 1)
    };
    if (dateFull.day == dateFull.dayNext.day){
        dateFull.dayNext.day = 1;
        dateFull.dayNext.month = dateFull.monthNext.month;
        dateFull.dayNext.year = dateFull.monthNext.year;
    }
    
    // Prev day
    let month = dateFull.month;
    if (dateFull.day == 1){
        month = dateFull.monthPrev.month
    }
    let year = dateFull.year;
    if (dateFull.day == 1) {
        year = dateFull.monthPrev.year
    }
   dateFull.dayPrev = {
        day: dateFull.day - 1,
        month: month,
        year: year
    }

    if (dateFull.day == 1 ){
        dateFull.dayPrev.day = 31;
       if (dateFull.dayPrev.month == 4
            || dateFull.dayPrev.month == 6
            || dateFull.dayPrev.month == 9
            || dateFull.dayPrev.month == 11
        ) {
            dateFull.dayPrev.day = 30
        };
        if (dateFull.dayPrev.month == 2) {
            dateFull.dayPrev.day = (dateFull.year % 4) ? 28 : 29
        };      
    }
    return (dateFull)
}