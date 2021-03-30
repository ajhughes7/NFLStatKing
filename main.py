import mysql.connector as mysql
import matplotlib.pyplot as plt

db = mysql.connect(
    host="localhost",
    user="root",
    passwd="capstone2021",
    database="NFLStatKing"
)
cursor = db.cursor()


#generateSite()
    #generateIndexPage()
    #for each team
        #generateTeamPage(team)
        #generateCharts(team)

nflTeams = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX',
            'KC', 'LV', 'LAC', 'LA', 'MIA', 'MIN', 'NE', 'NO', 'NYG', 'NYJ', 'PHI', 'PIT', 'SF', 'SEA', 'TB', 'TEN',
            'WAS']



def formationTendencies(offensiveTeam):
    formationQuery = """SELECT DISTINCT
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && Formation='SHOTGUN') as shotgunCount,   
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && Formation='UNDER CENTER') as underCenterCount,
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && Formation='NO HUDDLE SHOTGUN') 
            as noHuddleShotgunCount,
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && Formation='PUNT') as puntCount,
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && Formation='NO HUDDLE') as noHuddleCount
        FROM PlayByPlay2020"""
    tuple1 = (offensiveTeam,) * 5
    cursor.execute(formationQuery, tuple1)
    records = list(cursor.fetchall())
    fig = plt.figure()
    formations = ['Shotgun', 'Under Center', 'No Huddle Shotgun', 'Punt', 'No Huddle']
    plt.bar(formations, records[0])
    plt.title( f"{offensiveTeam} Offensive Formations")
    plt.xticks(size=7)
    plt.yticks(size=7)
    return fig


def rushDirection(offensiveTeam):
    rushDirectionQuery = """SELECT DISTINCT
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && RushDirection='LEFT TACKLE') as leftTackleCount,   
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && RushDirection='LEFT GUARD') as leftGuardCount,
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && RushDirection='LEFT END') as leftEndCount,   
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && RushDirection='CENTER') as centerCount,
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && RushDirection='RIGHT GUARD') as rightGuardCount,   
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && RushDirection='RIGHT TACKLE') as rightTackleCount,
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && RushDirection='RIGHT END') as rightEndCount   
        FROM PlayByPlay2020"""
    tuple1 = (offensiveTeam,) * 7
    cursor.execute(rushDirectionQuery, tuple1)
    records = list(cursor.fetchall())
    fig = plt.figure()
    rushDirections = ['LEFT END', 'LEFT TACKLE', 'LEFT GUARD', 'CENTER', 'RIGHT GUARD', 'RIGHT TACKLE', 'RIGHT END']
    plt.bar(rushDirections, records[0])
    plt.title(f"{offensiveTeam} Rushing Directions")
    plt.xticks(size=6)
    plt.yticks(size=6)
    return fig


def passType(offensiveTeam):
    rushDirectionQuery = """SELECT DISTINCT
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && PassType='LEFT TACKLE') as leftTackleCount,   
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && PassType='LEFT GUARD') as leftGuardCount,
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && PassType='LEFT END') as leftEndCount,   
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && PassType='CENTER') as centerCount,
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && PassType='RIGHT GUARD') as rightGuardCount,   
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && PassType='RIGHT TACKLE') as rightTackleCount,
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && PassType='RIGHT END') as rightEndCount   
        FROM PlayByPlay2020"""
    tuple1 = (offensiveTeam,) * 7
    cursor.execute(rushDirectionQuery, tuple1)
    records = list(cursor.fetchall())
    fig = plt.figure()
    rushDirections = ['LEFT END', 'LEFT TACKLE', 'LEFT GUARD', 'CENTER', 'RIGHT GUARD', 'RIGHT TACKLE', 'RIGHT END']
    plt.bar(rushDirections, records[0])
    plt.title( f"{offensiveTeam} Rushing Directions")
    plt.xticks(size=6)
    plt.yticks(size=6)
    return fig



def passVsRun(offensiveTeam):
    passVsRunQuery = """SELECT DISTINCT
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && PlayType='PASS') as passCount,   
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && PlayType='RUSH') as rushCount   
        FROM PlayByPlay2020"""
    tuple1 = (offensiveTeam,) * 2
    cursor.execute(passVsRunQuery, tuple1)
    records = list(cursor.fetchall())
    rushDirections = ['PASS', 'RUSH']
    fig, ax1 = plt.subplots()
    ax1.pie(records[0], labels=rushDirections, autopct='%.2f', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(f"{offensiveTeam} Pass vs Rush")
    return fig


def genTeamPage(fileName, nflTeam):
    htmlFile = open(fileName, "w")
    htmlFile.write(
        f"""
        <html>
            <head></head>
            <body>
                <h1>{nflTeam}</h1>
                <p><img src="{nflTeam}_formation.svg"></img></p>
                <p><img src="{nflTeam}_rush.svg"></img></p>
                <p><img src="{nflTeam}_PassVsRun.svg"></img></p>                            
            </body>
        </html>""")
    htmlFile.close()



def main():

    for nflTeam in nflTeams:
        print(nflTeam)
        genTeamPage(f"{nflTeam}.html", nflTeam)
        formationTendencies(nflTeam).savefig(f"{nflTeam}_formation.svg", format='svg')
        rushDirection(nflTeam).savefig(f"{nflTeam}_rush.svg", format='svg')
        passVsRun(nflTeam).savefig(f"{nflTeam}_PassVsRun.svg", format='svg')

main()

#formationTendencies('CLE')
#rushDirection('PIT')
#passVsRun('PIT')




#print(records)

#for record in records[0]:
    #print(record)







