

if __name__== '__main__':


    cmd = False
    cmd2 = True
    cmd3 = False

    while(cmd):
            query = raw_input('ios>')
            
            if query == 'exit':
                print "Exiting program"
                break
            

            print "Data values for OS: {0}.{1}.{2} ".format(x , xx if xx else "x" , xxx if xxx else "x")
            
            ioStat.generateStats(x,xx,xxx)

    while(cmd2):
        query = raw_input('android>')
        
        if query == 'exit':
            print "Exiting program"
            break
        
        x,xx,xxx = processOsVersion(query)
        #print "Data values for OS: {0}.{1}.{2} ".format(x , xx if xx else "x" , xxx if xxx else "x")
        
        result = androidStat.generateStats(x,xx,xxx,2)
        print result

    while(cmd3):
        query = raw_input('android-name>')
        
        if query == 'exit':
            print "Exiting program"
            break
        
        manufacturer, model = processAndroidModel(query, 1)
        print "Manufacturer: %s" % manufacturer
        print "Model: %s" % model
        print androidNS.returnName(manufacturer, model)
        
        #androidStat.generateStats(x,xx,xxx)