import datetime
from app import app, db
from flask import render_template, jsonify, request
from app.schema import Activity, Region, Ward, User, Seed

def store_activity(user_id:int, action:str):
    act = Activity(user_id=user_id, action=action)
    db.session.add(act)
    db.session.commit()

@app.route("/")
def home():
  """ Returns a page with a documentation about the API """
  return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
  """ API endpoint for user login """
  if request.method != "POST":
    return jsonify({"error":"method not allowed"}), 405

  try:
    # data = request.json
    data = request.form
    user = User.query.filter_by(phone=data["phone"], password=data["password"]).first()

    if not user:
      return jsonify({"error":"invalid phone or password"}), 401

    store_activity(user.id, "login")
    return jsonify({
      "token": {
        "fullname": user.fullname,
        "role": user.role,
        "id": user.id
      }
    })
  except Exception as error:
    print(error)
    return jsonify({"error": "username and password are required"}), 400

@app.route("/register", methods=["POST"])
def register():
  """ API endpoint for registering new farmer """
  if request.method != "POST":
    return jsonify({"error":"method not allowed"}), 405

  try:
    # data = request.json
    data = request.form
    user = User(fullname=data["fullname"], phone=data["phone"], ward_id=data["ward"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    print(data["fullname"])
    return jsonify({"success":"registered successfully"})
  except Exception as e:
    print(e)
    return jsonify({"error": "all fields are required"}), 400

@app.route("/regions", methods=["GET"])
def regions():
  """ API endpoint to list all regions in Tanzania """
  if request.method != "GET":
    return jsonify({"error":"method not allowed"}), 405

  reqions_query = Region.query.all()
  regions_list = []

  for region in reqions_query:
    regions_list.append({
      "id":region.id,
      "name":region.name
    })
  return jsonify(regions_list)

@app.route("/wards", methods=["GET"])
def wards():
  """ API endpoint to list all wards of a specific region in Tanzania """
  if request.method != "GET":
    return jsonify({"error":"method not allowed"}), 405

  try:
    region = request.args.get("region")
    wards_list = []
    selected_region = Region.query.filter(Region.name.like(region)).first()

    if not selected_region:
      return jsonify({"error":"invalid region name"})

    wards_query = selected_region.wards

    for ward in wards_query:
      wards_list.append({
        "id": ward.id,
        "name": ward.name
      })

    return jsonify(wards_list)
  except Exception as e:
    print(e)
    return jsonify({"error": "region query paramter is required"}), 400

@app.route("/verify", methods=["GET"])
def verify():
  """ API endpoint to verify if the given seed code is valid or not """
  if request.method != "GET":
    return jsonify({"error":"method not allowed"}), 405

  try:
    number = request.args.get("number")
    seed = Seed.query.filter_by(number=number).first()

    if not seed:
      return jsonify({
        "status": "fake",
        "data": "The seed is not recognized and thus it is fake"
      })

    return jsonify({
        "status": "original",
        "data": {
          "id": seed.id,
          "name": seed.name,
          "expire_date": seed.expire_date,
          "manufucturer": seed.manufucturer,
          "description": seed.description
        }
      })
  except Exception as e:
    print(e)
    return jsonify({"error": "number query paramter is required"}), 400


@app.route("/fill-region")
def fill_region():
  data = [
    { "type": "Feature", "properties": { "region": "Arusha" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Dar es Salaam" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Dodoma" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Geita" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Iringa" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Kagera" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Katavi" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Kigoma" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Kilimanjaro" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Lindi" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Manyara" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Mara" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Mbeya" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Morogoro" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Mtwara" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Mwanza" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Njombe" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Pemba Kaskazini" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Pemba Kusini" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Pwani" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Rukwa" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Ruvuma" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Shinyanga" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Simiyu" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Singida" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Songwe" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Tabora" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Tanga" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Unguja Kaskazini" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Unguja Mjini Magharibi" }, "geometry": "null" },
    { "type": "Feature", "properties": { "region": "Unguja Kusini" }, "geometry": "null" }
  ]

  for i in data:
    r = Region(name = i["properties"]["region"])
    db.session.add(r)
  db.session.commit()
  return "done!"

@app.route("/fill-wards")
def fill_wards():
  data = [
    {
      "name": "Arusha",
      "districts":[
              {
                    "name":"Arumeru Magharibi"
              },
                {
                  "name": "Arumeru Mashariki"
                },
                {
                  "name": "Arusha Mjini "
                },
                {
                "name":"Karatu"
              },
                {
                  "name": "Longido"
                },
                {
                  "name": "Monduli"
                }
              ]
    },
    {
      "name": "Dar es Salaam",
      "districts":[
              {
                    "name":"Kinondoni"
              },
                {
                  "name": "Temeke"
                },
                {
                  "name": "Ilala"
                },
                {
                "name":"Ubungo"
              },
                {
                  "name": "Kigamboni"
                }
              ]
    },
    {
      "name": "Dodoma",
      "districts":[
              {
                    "name":"Bahi"
              },
                {
                  "name": "Chamwino"
                },
                {
                  "name": "Chemba"
                },
                {
                "name":"Dodoma"
              },
                {
                  "name": "Kondoa"
                },
                {
                  "name": "Kongwa"
                },
                {
                  "name": "Mpwapwa"
                }
              ]
    },
    {
      "name": "Iringa",
      "districts":[
              {
                    "name":"Bahi"
              },
                {
                  "name": "Chamwino"
                },
                {
                  "name": "Chemba"
                },
                {
                "name":"Dodoma Mjini"
              },
              {
                "name":"Dodoma Vijijini"
              },
                {
                  "name": "Kondoa"
                },
                {
                  "name": "Kongwa"
                },
                {
                  "name": "Mpwapwa"
                }
              ]

    },
    {
      "name": "Kagera",
      "districts":[
              {
                    "name":"Biharamulo"
              },
                {
                  "name": "Bukoba Mjini"
                },
                {
                  "name": "Bukoba Vijijini"
                },
                {
                "name":"Karagwe"
              },
              {
                "name":"Missenyi"
              },
                {
                  "name": "Muleba"
                },
                {
                  "name": "Ngara"
                },
                {
                  "name": "Kyerwa"
                }
              ]
    },
    {
      "name": "Kaskazini Pemba",
      "districts":[
              {
                    "name":"Micheweni"
              },
                {
                  "name": "Wete"
                }
                
              ]
    },
    {
      "name": "Kaskazini Unguja",
      "districts":[
              {
                    "name":"Unguja Kaskazini A"
              },
                {
                  "name": "Unguja Kaskazini B"
                }
              ]
    },
    {
      "name": "Kigoma",
      "districts":[
              {
                    "name":"Kasulu"
              },
                {
                  "name": "Kibondo"
                },
                {
                  "name": "Kigoma Vijijini"
                },
                {
                "name":"Kigoma Mjini"
              },
              {
                "name":"Kigoma Ujiji"
              },
                {
                  "name": "Buhigwe"
                },
                {
                  "name": "Kakonko"
                },
                {
                  "name": "Uvinza"
                }
              ]
    },
    {
      "name": "Kilimanjaro",
      "districts":[
              {
                    "name":"Hai"
              },
                {
                  "name": "Moshi Mjini"
                },
                {
                  "name": "Moshi Vijijini"
                },
                {
                "name":"Mwanga"
              },
              {
                "name":"Rombo"
              },
                {
                  "name": "Same"
                },
                {
                  "name": "Siha"
                }
              ]
    },
    {
      "name": "Kusini Pemba",
      "districts":[
              {
                    "name":"Chake Chake"
              },
                {
                  "name": "Mkoani"
                }
              ]
    },
    {
      "name": "Kusini Unguja",
      "districts":[
              {
                    "name":"Kati Unguja"
              },
                {
                  "name": "Kusini Unguja"
                },
              ]
    },
    {
      "name": "Lindi",
      "districts":[
              {
                    "name":"Kilwa"
              },
                {
                  "name": "Lindi Mjini"
                },
                {
                  "name": "Lindi Vijijini"
                },
                {
                "name":"Nachingwea"
              },
              {
                "name":"Ruangwa"
              },
                {
                  "name": "Liwale"
                }
              ]
    },
    {
      "name": "Manyara",
      "districts":[
              {
                    "name":"Babati"
              },
                {
                  "name": "Babati Vijijini"
                },
                {
                "name":"Hanang"
              },
              {
                "name":"Kiteto"
              },
                {
                  "name": "Mbulu"
                },
                {
                  "name": "Simanjiro"
                }
              ]
    },
    {
      "name": "Mara",
      "districts":[
              {
                    "name":"Bunda"
              },
                {
                  "name": "Musoma Mjini"
                },
                {
                  "name": "Musoma Vijijini"
                },
                {
                "name":"Rorya"
              },
              {
                "name":"Serengeti"
              },
                {
                  "name": "Tarime"
                }
              ]
    },
    {
      "name": "Mbeya",
      "districts":[
              {
                    "name":"Chunya"
              },
                {
                  "name": "Ileje"
                },
                {
                  "name": "Kyela"
                },
                {
                "name":"Mbarali"
              },
              {
                "name":"Mbeya Mjini"
              },
                {
                  "name": "Mbeya Vijijini"
                },
                {
                  "name": "Mbozi"
                }
              ]
    },
    {
      "name": "Mjini Magharibi",
      "districts":[
              {
                    "name":"Magharibi Unguja"
              },
                {
                  "name": "Mjini Unguja"
                }
              ]
    },
    {
      "name": "Morogoro",
      "districts":[
              {
                    "name":"Gairo"
              },
                {
                  "name": "Morogoro Mjini"
                },
                {
                  "name": "Morogoro Vijijini"
                },
                {
                "name":"Kilombero"
              },
              {
                "name":"Kilosa"
              },
                {
                  "name": "Mvomero"
                },
                {
                  "name": "Malinyi"
                },
                {
                  "name": "Ulanga"
                }
              ]
    },
    {
      "name": "Mtwara",
      "districts":[
              {
                    "name":"Masasi"
              },
                {
                  "name": "Masasi Mjini"
                },
                {
                  "name": "Mtwara Mikindani"
                },
                {
                "name":"Mtwara Mjini"
              },
              {
                "name":"Mtwara Vijijini"
              },
                {
                  "name": "Newala"
                },
                {
                  "name": "Tandahimba"
                }
              ]

    },
    {
      "name": "Mwanza",
      "districts":[
              {
                    "name":"Geita"
              },
                {
                  "name": "Ilemela"
                },
                {
                  "name": "Kwimba"
                },
                {
                "name":"Magu"
              },
              {
                "name":"Misungwi"
              },
                {
                  "name": "Nyamagana"
                },
                {
                  "name": "Sengerema"
                },
                {
                  "name": "Ukerewe"
                }
              ]
    },
    {
      "name": "Pwani",
      "districts":[
              {
                    "name":"Bagamoyo"
              },
                {
                  "name": "Kibaha"
                },
                {
                  "name": "Kibiti"
                },
                {
                "name":"Kisarawe"
              },
              {
                "name":"Mafia"
              },
                {
                  "name": "Mkuranga"
                },
                {
                  "name": "Rufiji"
                },
              ]
    },
    {
      "name": "Rukwa",
      "districts":[
              {
                    "name":"Mpanda"
              },
                {
                  "name": "Nkansi"
                },
                {
                  "name": "Sumbawanga Mjini"
                },
                {
                "name":"Sumbawanga Vijijini"
              },
              {
                "name":"Kalambo"
              }
              ]
    },
    {
      "name": "Ruvuma",
      "districts":[
              {
                    "name":"Mbinga"
              },
                {
                  "name": "Namtumbo"
                },
                {
                  "name": "Songea Mjini"
                },
                {
                "name":"Songea Vijijini"
              },
              {
                "name":"Tunduru"
              },
                {
                  "name": "Nyasa"
                }
              ]
    },
    {
      "name": "Shinyanga",
      "districts":[
              {
                    "name":"Bariadi"
              },
                {
                  "name": "Shinyanga Mjini"
                },
                {
                  "name": "Shinyanga Vijijini"
                },
                {
                "name":"Bukombe"
              },
              {
                "name":"Kahama Mjini"
              },
                {
                  "name": "Kahama Vijijini"
                },
                {
                  "name": "Kishapu"
                },
                {
                  "name": "Maswa"
                },
                {
                  "name": "Meatu"
                }
              ]

    },
    {
      "name": "Singida",
      "districts":[
              {
                    "name":"Iramba"
              },
                {
                  "name": "Manyoni"
                },
                {
                  "name": "Singida Mjini"
                },
                {
                "name":"Singida Vijijini"
              },
              {
                "name":"Ikungi"
              },
                {
                  "name": "Mkalama"
                }
              ]
    },
    {
      "name": "Tabora",
      "districts":[
              {
                    "name":"Igunga"
              },
                {
                  "name": "Tabora Mjini"
                },
                {
                  "name": "Nzega"
                },
                {
                "name":"Sikonge"
              },
              {
                "name":"Urambo"
              },
                {
                  "name": "Uyui"
                },
                {
                  "name": "Kaliua"
                }
              ]
    },
    {
      "name": "Tanga",
      "districts":[
              {
                    "name":"Handeni"
              },
                {
                  "name": "Handeni Mjini"
                },
                {
                  "name": "Handeni Vijijini"
                },
                {
                "name":"Korogwe"
              },
              {
                "name":"Lushoto"
              },
                {
                  "name": "Mkinga"
                },
                {
                  "name": "Muheza"
                },
                {
                  "name": "Pangani"
                },{
                  "name":"Tanga"
                }
              ]
    }
  ]

  for i in data:
    current_region = i["name"]
    db_region = Region.query.filter(Region.name.like(current_region)).first()

    if db_region:
      for curr_ward in i["districts"]:
        w = Ward(name=curr_ward["name"],region_id=db_region.id)
        db.session.add(w)
    else:
      print(f"Failed for {current_region}")
  
  db.session.commit()
  return "done!"

@app.route("/fill-seeds")
def fill_seeds():
  data = [
    {"name":"Maize", "desc": "A warm-season crop with yellow or white kernels grown for human or animal consumption. Major producers include SeedCo, Pannar Seed, and Monsanto."},
    {"name":"Rice", "desc": "A warm-season crop with seeds used as a staple food in many cultures. Major producers include Tanzania Agricultural Research Institute (TARI), National Irrigation Commission (NIRC), and Kilombero Plantations Limited."},
    {"name":"Beans", "desc": "A warm-season legume crop with high protein content, commonly used for human consumption. Major producers include Selian Agricultural Research Institute (SARI), Tanzania Seed Company (TANSEED), and Matengo Seed Company."},
    {"name":"Sorghum", "desc": "A warm-season cereal crop with seeds used for animal feed, human consumption, and biofuels. Major producers include SAGCOT Initiative, Tanzania Seed Company, and Kilimo Trust."},
    {"name":"Sunflower", "desc": "A warm-season crop with large flower heads containing edible seeds and oil. Major producers include Tanzania Seed Company, Kenya Seed Company, and SeedCo."},
    {"name":"Cotton", "desc": "A warm-season crop grown for its fibers, which are used to make textiles and clothing. Major producers include Tanzania Cotton Board, Alliance Ginneries Ltd., and Newala Co-operative Union Ltd."},
    {"name":"Peanuts", "desc": "A warm-season legume crop with high protein content, commonly used for human consumption. Major producers include Tanzania Agricultural Research Institute, Tanzania Seed Company, and Uyole Agricultural Research Institute."},
    {"name":"Sesame", "desc": "A warm-season crop with edible seeds used for human consumption and oil. Major producers include Tanzania Seed Company, Kilimo Trust, and SeedCo."},
    {"name":"Soybean", "desc": "A warm-season legume crop with high protein content, commonly used for animal feed and processed foods. Major producers include Tanzania Seed Company, Sokoine University of Agriculture, and SeedCo."},
    {"name":"Cassava", "desc": "A warm-season root crop with edible tubers used for human consumption. Major producers include Sokoine University of Agriculture, Ministry of Agriculture, and Tanzania Agricultural Research Institute."},
    {"name":"Sweet potatoes", "desc": "A warm-season root crop with edible tubers used for human consumption. Major producers include Sokoine University of Agriculture, Tanzania Agricultural Research Institute, and Ministry of Agriculture."},
    {"name":"Sugarcane", "desc": "A warm-season crop with edible stems used for human consumption and sugar production. Major producers include Kilombero Sugar Company, Kagera Sugar Limited, and Mtibwa Sugar Estates."},
    {"name":"Millet", "desc": "A warm-season cereal crop with seeds used for human consumption and animal feed. Major producers include Tanzania Seed Company, Kilimo Trust, and SeedCo."},
    {"name":"Groundnuts", "desc": "A warm-season legume crop with high protein content, commonly used for human consumption. Major producers include Tanzania Seed Company, Sokoine University of Agriculture, and SeedCo."},
    {"name":"Vegetables", "desc": "Various cool-season and warm-season crops with edible parts used for human consumption. Major producers include Tanzania Horticultural Association, Tanzanian Agri-business and SMEs Organization, and Selian Agricultural Research Institute."}
  ]

  val = 0
  for i in data:
    s = Seed(name=i["name"], number=f"123{val}", description=i["desc"], expire_date=datetime.datetime.now(), manufucturer=f"Company {val+1}")
    db.session.add(s)
    val += 1
  db.session.commit()

  return "done!"

