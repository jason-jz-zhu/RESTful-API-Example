from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/test'
db = SQLAlchemy(app)



###Models####
class Account(db.Model):
    __tablename__ = "flask"
    name = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(20))

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,name,account):
        self.name = name
        self.account = account
    def __repr__(self):
        return '' % self.id
db.create_all()

class AccountSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Account
        sqla_session = db.session
    name = fields.String(required=True)
    account = fields.Number(required=True)

@app.route('/people/<name>-<discount>-<price>', methods = ['POST'])
def get_info_by_name(name, discount, price):
    get_account = Account.query.get(name)
    account_schema = AccountSchema()
    result = account_schema.dump(get_account)
    total_money = result["account"]
    name = result["name"]
    need_price = int(price) * int(discount) / 100
    can_buy = "yes" if total_money > int(price) else "no"
    return make_response(jsonify({"can_buy?": can_buy}))

if __name__ == "__main__":
    app.run(debug=True)