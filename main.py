import mysql.connector as mysql
import matplotlib.pyplot as plt
import numpy as np

db = mysql.connect(
    host="localhost",
    user="root",
    passwd="capstone2021",
    database="NFLStatKing"
)
cursor = db.cursor()


#generateSite()      Brandon
    #generateIndexPage()  Brandon
    #for each team                      Hunter
        #generateTeamPage(team)  AJ
        #generateCharts(team)     AJ

nflTeams = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX',
            'KC', 'LV', 'LAC', 'LA', 'MIA', 'MIN', 'NE', 'NO', 'NYG', 'NYJ', 'PHI', 'PIT', 'SF', 'SEA', 'TB', 'TEN',
            'WAS']

#nflTeams = ['PIT']


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
    shortPassQuery = """SELECT DISTINCT
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && PassType='SHORT LEFT') as shortLeftCount,   
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && PassType='SHORT MIDDLE') as shortMiddleCount,   
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && PassType='SHORT RIGHT') as shortRightCount   
        FROM PlayByPlay2020"""
    deepPassQuery = """SELECT DISTINCT
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && PassType='DEEP LEFT') as deepLeftCount,
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && PassType='DEEP MIDDLE') as deepMiddleCount,
        (SELECT COUNT(*) FROM PlayByPlay2020 WHERE OffenseTeam=%s && PassType='DEEP RIGHT') as deepRightCount
        From PlayByPlay2020"""
    tuple1 = (offensiveTeam,) * 3
    cursor.execute(shortPassQuery, tuple1)
    records1 = list(cursor.fetchall())
    cursor.execute(deepPassQuery, tuple1)
    records2 = list(cursor.fetchall())
    fig = plt.figure()
    w = 0.4
    passDirections = ['LEFT', 'MIDDLE', 'RIGHT']
    shortBar = np.arange(len(passDirections))
    deepBar = [i+w for i in shortBar]
    plt.bar(shortBar, records1[0], w, label="SHORT")
    plt.bar(deepBar, records2[0], w, label="DEEP")
    plt.title(f"{offensiveTeam} Pass Type Tendencies")
    plt.xticks(shortBar+w/2, passDirections, size=6)
    plt.yticks(size=6)
    plt.legend()
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

'''
def qbCompletions():
    qbCompletionsQuery = """SELECT DISTINCT
        (SELECT SUBSTRING(DESCRIPTION, 3, 6) FROM PlayByPlay2020 WHERE OffenseTeam='PIT' && PlayType='PASS') as passer,   
        (SELECT SUBSTRING(DESCRIPTION, 3, 6) FROM PlayByPlay2020 WHERE OffenseTeam='PIT' && PlayType='RUSH') as rusher   
        FROM PlayByPlay2020"""
    cursor.execute(qbCompletionsQuery)
    records = list(cursor.fetchall())
    for record in records[0]:
        print(record)
'''

'''
    tuple1 = (offensiveTeam,) * 2

    rushDirections = ['PASS', 'RUSH']
    fig, ax1 = plt.subplots()
    ax1.pie(records[0], labels=rushDirections, autopct='%.2f', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(f"{offensiveTeam} Pass vs Rush")
    return fig
    '''



def genTeamPage(fileName, nflTeam):
    htmlFile = open(fileName, "w")
    htmlFile.write(
        f"""
        <html>
            <head></head>
            <body>
                <h1>{nflTeam}</h1>
                <p><img src="{nflTeam}_Formation.svg"></img></p>
                <p><img src="{nflTeam}_Rush.svg"></img></p>
                <p><img src="{nflTeam}_PassVsRun.svg"></img></p>                            
                <p><img src="{nflTeam}_PassType.svg"></img></p>                            
            </body>
        </html>""")
    htmlFile.close()

#qbCompletions()

def main():

    for nflTeam in nflTeams:
        print(nflTeam)
        genTeamPage(f"{nflTeam}.html", nflTeam)
        formationTendencies(nflTeam).savefig(f"{nflTeam}_Formation.svg", format='svg')
        rushDirection(nflTeam).savefig(f"{nflTeam}_Rush.svg", format='svg')
        passVsRun(nflTeam).savefig(f"{nflTeam}_PassVsRun.svg", format='svg')
        passType(nflTeam).savefig(f"{nflTeam}_PassType.svg", format='svg')


main()

#formationTendencies('PIT')
#rushDirection('PIT')
#passVsRun('PIT')
#passType('PIT')



#print(records)









