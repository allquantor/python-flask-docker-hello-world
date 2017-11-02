import boto3
from flask import Flask

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb')
table_coordinates = 'coordinates'


def dbCreateCoordinates(coordinate, name):
    client = boto3.client('dynamodb')
    existing_tables = client.list_tables()['TableNames']
    table = None

    if table_coordinates not in existing_tables:
        # Create the DynamoDB table.
        table = createCoordinatesTable()
    else:
        table = dynamodb.Table(table_coordinates)

    table.put_item(
            Item={
                'coordinate': coordinate,
                "name": name
            }
    )
    print "We did it! Coordinates Inserted"


def dbGetCoordinates(name):
    from boto3.dynamodb.conditions import Attr
    table = dynamodb.Table(table_coordinates)
    response = table.scan(
            FilterExpression=Attr('name').eq(name)
    )

    coordinate = response['Items']
    return 'Coordinate for' + 'name is' + str(coordinate)


def createCoordinatesTable():
    table = dynamodb.create_table(
            TableName=table_coordinates,
            KeySchema=[
                {
                    'AttributeName': 'coordinate',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'name',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'coordinate',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'name',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            })

    # Ahhhh evil blocking here!!!!
    print "Creating Table... Waiting....."
    table.meta.client.get_waiter('table_exists').wait(TableName=table_coordinates)
    return table


@app.route("/")
def hello():
    return "Hello, from Python in Docker!!"


@app.route('/create/<float:coordinate>/<string:name>')
def createCoordinate(coordinate, name):
    import decimal
    dbCreateCoordinates(decimal.Decimal(str(coordinate)), name)
    return 'Coordinates for ' + name + ' with value:  %d'  %coordinate + ' are created.'


@app.route('/get/<string:name>')
def getCoordinates(name):
    return dbGetCoordinates(name)


@app.route("/")
def getRoute():
    return "Hello, from Python in Docker!!"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
