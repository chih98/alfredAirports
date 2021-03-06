# -*- coding: utf-8 -*-

import sys
from workflow import Workflow3, web
from workflow.background import is_running
from downloadDataFiles import string_from_percent, build_wf_entry
# Airprot with autolookup

# Data source: http://ourairports.com/data/airports.csv

def main(wf):
    query = str(wf.args[0]).lower()
    log.debug(query)

    code_match = []
    name_match = []
    other_match = []

    import os.path
    if not os.path.exists('airports.csv'):
        if is_running('bg'):
            pct = None
            while pct is None:
                try:
                    pct = wf.stored_data('download_percent')
                except:
                    pass

            progress = wf.stored_data('download_progress')
            file = wf.stored_data('download_file')

            wf.rerun = 0.5

            title = "Please wait for data file downloads to complete"
            subtitle = progress + " " + string_from_percent(pct) + " " + str(pct) + "%"
            wf.add_item(title, subtitle=subtitle)
        else:
            wf.add_item('No data files','Run "aptinit" to get airport database', icon="images/evil.png", arg="aptinit")

        wf.send_feedback()
        return


    # "id","ident","type","name","latitude_deg","longitude_deg","elevation_ft","continent","iso_country","iso_region","municipality","scheduled_service","gps_code","iata_code","local_code","home_link","wikipedia_link","keywords"
    with open('airports.csv', 'r') as airport_file:
        next(airport_file)  # Skip first line
        for line in airport_file:
            line = line.rstrip('\n')
            if query in line.lower():

                parts = line.split(',')
                apt_id = parts[0].replace('"','')
                icao = parts[1].replace('"','')
                apt_type = parts[2].replace('"','')
                name = parts[3].replace('"','')
                latitude_deg = parts[4].replace('"','')
                longitude_deg = parts[5].replace('"','')
                elevation_ft = parts[6].replace('"','')
                continent = parts[7].replace('"','')
                iso_country = parts[8].replace('"','')
                iso_region = parts[9].replace('"','')
                municipality = parts[10].replace('"','')
                scheduled_service = parts[11].replace('"','')
                gps_code = parts[12].replace('"','')
                iata_code = parts[13].replace('"','')
                local_code = parts[14].replace('"','')
                home_link = parts[15].replace('"','')
                wikipedia_link = parts[16].replace('"','')
                keywords = filter(None, [e.replace('"','') for e in parts[17:]])

                # print icao, iata_code, local_code, name, home_link, wikipedia_link
                codes = filter(None, set([icao, iata_code, gps_code, local_code]))




                # print name, codes
                # \\U0001F1F2\\U0001F1FD\\U0000FE0F
                flag = ""
                if len(iso_country) > 1:
                    l1 = str(hex(ord(iso_country[0]) + 127397)[2:]).upper()
                    l2 = str(hex(ord(iso_country[1]) + 127397)[2:]).upper()
                    flag = "\\U000{}\\U000{}\\U0000FE0F".format(l1, l2)
                # print iso_country, flag.decode('unicode_escape')

                subtitle = ", ".join(codes) + " " + apt_type

                if len(keywords) > 0:
                    subtitle += " [" + ', '.join(keywords) + "]"

                title = str(name).decode('utf-8', 'ignore') + " " + flag.decode('unicode_escape')
                arg = icao
                valid = 'True'

                value_map = {'subtitle':subtitle, 'title':title, 'arg':arg, 'valid':valid, 'icon':"images/{}.png".format(apt_type)}




                if any(filter(lambda x: query.upper() in x, codes)):
                    code_match.append(value_map)
                elif query.upper() in name.upper():
                    name_match.append(value_map)
                else:
                    other_match.append(value_map)

        # Build ordered search results
        for i in code_match:
            wf.add_item(**i)
        for i in name_match:
            wf.add_item(**i)
        for i in other_match:
            wf.add_item(**i)

    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
