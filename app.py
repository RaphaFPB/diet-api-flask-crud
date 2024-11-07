from flask import Flask,request,jsonify
from database import db
from models.meal import Meal
from datetime import datetime


app= Flask(__name__)
app.config['SECRET_KEY'] = ["your_secret_key"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


db.init_app(app)

@app.route('/diets', methods=['POST'])
def create_Meal():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    datetime_str = data.get("datetime")
    in_diet = data.get("in_diet")

    # Utiliza o valor fornecido ou o padrão do banco de dados (func.now()) para datetime
    datetime_obj = datetime.fromisoformat(datetime_str) if datetime_str else None

    
    if name and description:
        new_Meal=Meal(name=name, description=description,datetime=datetime_obj,in_diet=in_diet)
        db.session.add(new_Meal)
        db.session.commit()
        return jsonify({"message": "Refeição cadastrada na dieta com sucesso!"})
    return jsonify({"message": "Dados inválidos"}), 400
    
@app.route('/diets/<int:meal_id>', methods=['GET'])
def read_Meal(meal_id):
    meal = Meal.query.get(meal_id)#obter objeto meal da database através do id
    if not meal:
        return jsonify({"message": "Refeição não encontrada."}),404
    meal_data={
        "id":meal_id,
        "name":meal.name,
        "description":meal.description,
        "datetime":meal.datetime.strftime("%Y-%m-%dT%H:%M:%S"),
        "in_diet":meal.in_diet
    }
    return jsonify(meal_data)

@app.route('/diets', methods=['GET'])
def read_Meals():
    meals = Meal.query.all()#retorna todas as refeições cadastradas
    meal_list=[]
    if not meals:
         return jsonify({"message": "Não há refeições cadastradas."}), 404
    else:
        for meal in meals:
            meal_data ={
                "id":meal.id,
                "name":meal.name,
                "description":meal.description,
                "datetime":meal.datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "in_diet":meal.in_diet
            }
            meal_list.append(meal_data)
        return jsonify(meal_list)

@app.route('/diets/<int:meal_id>', methods=['PUT'])
def update_Meal(meal_id):
    data = request.json
    meal = Meal.query.get(meal_id)
    if not meal:
        return jsonify({"message": "Refeição não encontrada."}), 404
    meal.name = data.get("name", meal.name)#mantém valor atual se o usuário não inserir nada
    meal.description = data.get("description", meal.description)
    meal.in_diet = data.get("in_diet", meal.in_diet)
    datetime_str = data.get("datetime")#recebe a data e hora
    if datetime_str:#checa se o usuario enviou data e hora
        try:
            meal.datetime= datetime.fromisoformat(datetime_str)#converte para o formato correto
        except ValueError:
            return jsonify({"message": "Formato de data e hora inválido"}), 400
    db.session.commit()
    return jsonify({"message": f"Refeição {meal_id} atualizada com sucesso!"})

@app.route('/diets/<int:meal_id>', methods=['DELETE'])
def delete_Meal(meal_id):
    meal = Meal.query.get(meal_id)
    if meal:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": f"Refeição {meal_id} deletada com sucesso!"})
    
    return jsonify({"message": "Refeição não encontrada."}), 404
if __name__=='__main__':
    app.run(debug=True)


#Descobrir quando usar o db.session.commit() com flask shell
#verificar nomeação dos arquivos e classes Daily Diet API