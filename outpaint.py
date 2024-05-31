selection=[[386,720],[537,119]]
wp=[[0,0],[500,300]]
DISPLACE_X=0
DISPLACE_Y=-20
selection=[[selection[0][0]-wp[0][0],selection[0][1]-wp[0][1]],selection[1]]

def line_repos(l):
    global selection,DISPLACE_Y,DISPLACE_X
    rect=l[0]
    rect=[[c[0]+selection[0][0],c[1]+selection[0][1]] for c in rect]
    DISPLACE_Y=-1*(rect[2][1]-rect[1][1])
    w=rect[1][0]-rect[0][0]+DISPLACE_X
    h=rect[2][1]-rect[1][1]
    l[0]=[rect[0],[w,h]]
    ratios=get_word_ratios(l[1][0])
    wths=list(map(lambda x:x*w,ratios))
    i=rect[0][0]
    posxs=[]
    for www in wths:
        posxs.append(i)
        i=i+www+2
    wds=l[1][0].split(" ")
    i=0
    res=[]
    for w in wds:
        res.append([w,[posxs[i]+DISPLACE_X,rect[0][1]+DISPLACE_Y],[wths[i],h]])
    return res

def get_word_ratios(s):
    l=len(''.join(s.split(" ")))
    r=list(map(lambda x:(1+len(x))/l, s.split(" ")))
    return r


lines=[[[[50.0, 60.0], [460.0, 60.0], [460.0, 76.0], [50.0, 76.0]], ('In the spring of 2020, when the C0vID-19 pandemic swept', 0.9478289484977722)],
    [[[36.0, 78.0], [472.0, 79.0], [472.0, 98.0], [36.0, 97.0]], ('across the globe, the impact was felt by numerous industries,', 0.9571513533592224)],
    [[[45.0, 79.0], [460.0, 80.0], [460.0, 96.0], [45.0, 95.0]], ('including airlines, hotels, cruise operators, and restaurants.', 0.963908851146698)]]

rect=lines[0][0]
text=lines[0][1][0]
print(rect)
print(text)
print(sum([line_repos(l) for l in lines],[]))
print(len(text))
#[ for l in lines]
v=[[[[[113.0, 61.0], [398.0, 61.0], [398.0, 74.0], [113.0, 74.0]], ('The1917 revolution and the ensuing civil', 0.9343322515487671)], [[[115.0, 81.0], [393.0, 81.0], [393.0, 94.0], [115.0, 94.0]], ('war in Russia wouldbe a qood example', 0.921046793460846)]]]
[print(e) for e in v[0]]
[
    [
        ['They', [460.0, 783.0], [501.86046511627904, 799.0]],
        ["can't", [460.0, 783.0], [501.86046511627904, 799.0]],
        ['be', [460.0, 783.0], [501.86046511627904, 799.0]],
        ['bothered', [460.0, 783.0], [501.86046511627904, 799.0]],
        ['with', [460.0, 783.0], [501.86046511627904, 799.0]],
        ['your', [460.0, 783.0], [501.86046511627904, 799.0]],
        ['dealings', [460.0, 783.0], [501.86046511627904, 799.0]],
        ['anymore.', [460.0, 783.0], [501.86046511627904, 799.0]]
    ]]