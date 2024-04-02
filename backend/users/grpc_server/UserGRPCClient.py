import grpc
import user_pb2
import user_pb2_grpc
import traceback
from google.protobuf import json_format
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

channel = grpc.insecure_channel('localhost:50052')
stub = user_pb2_grpc.UsersStub(channel)

class UpdateUserInfo(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    contact_number: str | None = None
    postal_code: str | None = None

@app.get("/{uid}/borrowed_books")
def get_borrowed_books(uid: str):
    request = user_pb2.UID(uid=uid)

    try:
        response = stub.GetBorrowedBooks(request)
        print("GetBorrowedBooks Response: ", response)

        data = json_format.MessageToDict(response)
        return data
    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()
        raise HTTPException(500, "Internal server error")

@app.get("/{uid}/recommendations")
def get_recommendations(uid: str):
    request = user_pb2.UID(uid=uid)

    try:
        response = stub.GetRecommendations(request)
        print("GetRecommendations Response: ", response)

        data = json_format.MessageToDict(response)
        return data
    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()
        raise HTTPException(500, "Internal server error")

@app.get("/{uid}/waitlist")
def get_waitlist(uid: str):
    request = user_pb2.UID(uid=uid)

    try:
        response = stub.GetWaitlist(request)
        print("GetWaitlist Response: ", response)

        data = json_format.MessageToDict(response)
        return data
    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()
        raise HTTPException(500, "Internal server error")

@app.post("/{uid}/waitlist/{isbn}")
def append_to_waitlist(uid: str, isbn: str):
    request = user_pb2.UID_ISBN(uid=uid, isbn=isbn)

    try:
        response = stub.AppendToWaitlist(request)
        print("AppendToWaitlist Response: ", response)

        print(response.success)

        data = json_format.MessageToDict(response)

        if 'errorCode' in data:
            raise HTTPException(data['errorCode'], data['message'])

        return data
    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()
        raise HTTPException(500, "Internal server error")

@app.delete("/{uid}/waitlist/{isbn}")
def delete_from_waitlist(uid: str, isbn: str):
    request = user_pb2.UID_ISBN(uid=uid, isbn=isbn)

    try:
        response = stub.DeleteFromWaitlist(request)
        print("DeleteFromWaitlist Response: ", response)

        data = json_format.MessageToDict(response)

        if 'errorCode' in data:
            raise HTTPException(data['errorCode'], data['message'])

        return data
    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()
        raise HTTPException(500, "Internal server error")

@app.get("/users")
def get_all_users_info():
    request = user_pb2.EmptyInfo()

    try:
        response = stub.GetAllUsersInfo(request)
        print("GetAllUsersInfo Response: ", response)

        data = json_format.MessageToDict(response)

        if 'errorCode' in data:
            raise HTTPException(data['errorCode'], data['message'])

        return data
    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()
        raise HTTPException(500, "Internal server error")

@app.get("/users/{uid}")
def get_user_info(uid: str):
    request = user_pb2.UID(uid=uid)

    try:
        response = stub.GetUserInfo(request)
        print("GetUserInfo Response: ", response)

        data = json_format.MessageToDict(response)

        if 'errorCode' in data:
            raise HTTPException(data['errorCode'], data['message'])

        return data
    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()
        raise HTTPException(500, "Internal server error")
    
@app.put("/users/{uid}")
def update_user_info(uid: str, u_info: UpdateUserInfo):
    req_data = u_info.dict()
    request = json_format.ParseDict({'uid':uid} | req_data, user_pb2.UpdateUserInfoRequest())

    print({'uid':uid} | req_data)

    try:
        response = stub.UpdateUserInfo(request)
        print("UpdateUserInfo Response: ", response)

        data = json_format.MessageToDict(response)

        if 'errorCode' in data:
            raise HTTPException(data['errorCode'], data['message'])

        return data
    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()
        raise HTTPException(500, "Internal server error")
    
@app.delete("/users/{uid}")
def delete_user(uid: str):
    request = user_pb2.UID(uid=uid)

    try:
        response = stub.DeleteUser(request)
        print("DeleteUser Response: ", response)

        data = json_format.MessageToDict(response)

        if 'errorCode' in data:
            raise HTTPException(data['errorCode'], data['message'])

        return data
    except grpc.RpcError as e:
        print(f"RPC failed with code {e.code()}: {e.details()}")
        traceback.print_exc()
        raise HTTPException(500, "Internal server error")