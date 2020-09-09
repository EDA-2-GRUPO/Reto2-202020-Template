f = ([('id;actor1_name;actor1_gender;actor2_name;actor2_gender;actor3_name;actor3_gender;actor4_name;actor4_gender;actor5_name;actor5_gender;actor_number;director_name;director_gender;director_number;producer_name;producer_number;screeplay_name;editor_name', '13;Tom Hanks;2;Robin Wright;1;Gary Sinise;2;Mykelti Williamson;2;Sally Field;1;67;Robert Zemeckis;2;1;Wendy Finerman;3;Eric Roth;Arthur Schmidt')])
w = f[0][0].split(";")
x = f[0][1].split(";")
z = []
n=-1
for _ in w:
    n+=1
    z.append((w[n], x[n]))
print(w)
print(x)
print(z)