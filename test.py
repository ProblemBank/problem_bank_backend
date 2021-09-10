# import csv
# from Account.serializers import CreateUserSerializer 
# with open('g4g.csv') as f:
#     reader = csv.reader(f)
#     print(reader)

#     for row in reader:
#         data = {}
#         data['password'] = row[0]
#         data['username'] = row[4]
#         data['first_name'] = row[2]
#         data['last_name'] = row[3]
#         data['phone_number'] = row[4]
#         serializer = CreateUserSerializer(data=data)
#         data = serializer.validated_data
#         user = serializer.create(data)
#         user.save()

        #0pas 1team 2first 3last 4user