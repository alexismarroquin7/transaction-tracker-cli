import os;
import json;
import datetime;

def menu_input (**config):
  
  prompt = config["prompt"] if "prompt" in config else "";
  options = config["options"] if "options" in config else [];
  error_message = config["error_message"] if "error_message" in config else "\nInvalid input\n";
  initial_response = config["initial_response"] if "initial_response" in config else None;
  
  if (prompt == ""):
    prompt += "\n";

    for opt in options:
      prompt += f'{opt["in"]}) {opt["out"]}\n';
    
    prompt += "\n";

  response = initial_response;
  running = True;
  while(running):
    if(response != initial_response):
      print(error_message);
    
    response = input(prompt)

    for opt in options:
      if (response == opt["in"]):
        response = opt["out"];
        print("\n");
        running = False;
        break;

  return response;



class TransactionTracker () :
  def __init__(self, **config):
    file_name = config["file_name"] if "file_name" in config else "data";
    self.file_path = f"{file_name}.json";

  def setup (self):
    is_file = os.path.isfile(self.file_path);

    if(not is_file):
      f = open(self.file_path, "w");
      
      data = {
        "transactions": []
      };

      json.dump(data, f, indent = 2);

      f.close();

  def get_transactions (self):
    f = open (self.file_path, "r");

    data = json.loads(f.read());
    
    f.close();

    return data["transactions"];

  def set_transactions (self, trx_list):
    
    f = open (self.file_path, "r");
    data = json.loads(f.read());
    f.close();

    f = open(self.file_path, "w");
    
    newData = {
      **data,
      "transactions": trx_list
    }

    json.dump(newData, f, indent = 2);
    
    f.close();

    return self.get_transactions();

  def get_transaction_by_id (self, id):
    trx_list = self.get_transactions();
    
    trx_to_use = None;

    for trx in trx_list:
      if(trx["id"] == id):
        trx_to_use = trx;
        break;
    
    return trx_to_use;

  def create_deposit (self):
    print("Creating deposit...");
    name = input("Enter name: ");
    description = input("Enter description: ");
    amount = input("Enter amount: ");
    timestamp = datetime.datetime.now();

    trx_list = self.get_transactions();

    id = None;
    
    if(len(trx_list) == 0):
      id = 1;
    else:
      id = trx_list[-1]["id"] + 1;

  
    trx_list.append({
      "id": id,
      "name": name,
      "description": description,
      "amount": float(amount),
      "timestamp": str(timestamp),
      "type": "deposit"
    });

    self.set_transactions(trx_list);

  def create_withdrawal (self):
    print("Creating withdrawal...");
    name = input("Enter name: ");
    description = input("Enter description: ");
    amount = input("Enter amount: ");
    timestamp = datetime.datetime.now();

    trx_list = self.get_transactions();
    
    id = None;
    
    if(len(trx_list) == 0):
      id = 1;
    else:
      id = trx_list[-1]["id"] + 1;
    
    trx_list.append({
      "id": id,
      "name": name,
      "description": description,
      "amount": float(amount),
      "timestamp": str(timestamp),
      "type": "withdrawal"
    });

    self.set_transactions(trx_list);

  def create (self):
    print("What type of transaction do you want to make?");
    trx_type = menu_input(
      options = [
        {
          "in": "1",
          "out": "deposit"
        },
        {
          "in": "2",
          "out": "withdrawal"
        },
      ]
    );

    if(trx_type == "deposit"):
      self.create_deposit();
    elif(trx_type == "withdrawal"):
      self.create_withdrawal();
  
  def filter_by_type (self, type):
    trx_list = self.get_transactions();
    
    filtered_by_type = [];

    for trx in trx_list:
      if(trx["type"] == type):
        filtered_by_type.append(trx);

    return filtered_by_type;

  def print_transactions(self, transaction_list):
    print('id | timestamp | type | amount | name | description');

    balance = 0;
    deposit_count = 0;
    withdrawal_count = 0;

    for trx in transaction_list:
      s = f'{trx["id"]} | {trx["timestamp"]} | {trx["type"]} | {trx["amount"]} | {trx["name"]} | {trx["description"]}';
      print(s);

      if(trx["type"] == "deposit"):
        balance += trx["amount"];
        deposit_count += 1;
      elif(trx["type"] == "withdrawal"):
        balance += (trx["amount"] * -1);
        withdrawal_count += 1;
    
    print(f'balance: {balance} | deposits: {deposit_count} | withdrawals: {withdrawal_count} | total: {deposit_count + withdrawal_count}');

  def view_by_type (self):
    type_to_use = menu_input(
      options = [
        {
          "in": "1",
          "out": "deposit"
        },
        {
          "in": "2",
          "out": "withdrawal"
        }
      ]
    );

    self.print_transactions(self.filter_by_type(type_to_use));
    
  def view_all (self):
    trx_list = self.get_transactions();
    self.print_transactions(trx_list);
    

  def view (self):
    print('Select view option: ');
    menu_option = menu_input(
      options = [
        {
          "in": "1",
          "out": "all"
        },
        {
          "in": "2",
          "out": "filter by transaction type"
        }
      ]
    )

    if(menu_option == "all"):
      self.view_all();
    elif(menu_option == "filter by transaction type"):
      self.view_by_type();
    

  def delete_transaction_by_id (self, id):
    trx = self.get_transaction_by_id(id);
    if(trx == None): 
      print(f'transaction of id: {id} does not exist')
      return;

    trx_list = self.get_transactions();
    
    new_trx_list = [];

    for trx_item in trx_list:
      if(trx_item["id"] != trx["id"]):
        new_trx_list.append(trx_item);
    
    self.set_transactions(new_trx_list);

  def main_menu(self):
    menu_option = menu_input(
      options = [
        {
          "in": "1",
          "out": "create"
        },
        {
          "in": "2",
          "out": "view"
        },
        {
          "in": "3",
          "out": "update"
        },
        {
          "in": "4",
          "out": "delete"
        },
      ]
    );

    if(menu_option == "create"):
      self.create();
    elif(menu_option == "view"):
      self.view();
    elif(menu_option == "delete"):
      id = input('Enter id: ');
      self.delete_transaction_by_id(int(id));
  def run (self):
    
    self.setup();

    print('Transaction Tracker CLI');

    self.main_menu();

