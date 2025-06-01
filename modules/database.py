"""
Supabase 資料庫連接模組
處理與 Supabase 資料庫的所有連接和基本操作
"""

import os
from typing import Dict, List, Optional, Any
from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit as st

# 載入環境變數
load_dotenv()

class SupabaseManager:
    """Supabase 資料庫管理類別"""
    
    def __init__(self):
        """初始化 Supabase 連接"""
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.service_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("Supabase URL 和 Key 必須在環境變數中設定")
        
        # 建立客戶端連接
        self.client: Client = create_client(self.url, self.key)
        self.admin_client: Client = create_client(self.url, self.service_key) if self.service_key else None
        
    def test_connection(self) -> bool:
        """測試資料庫連接"""
        try:
            # 嘗試查詢用戶表格
            result = self.client.table("users").select("count", count="exact").execute()
            return True
        except Exception as e:
            print(f"資料庫連接測試失敗: {e}")
            return False
    
    def get_client(self) -> Client:
        """取得 Supabase 客戶端"""
        return self.client
    
    def get_admin_client(self) -> Client:
        """取得管理員權限的 Supabase 客戶端"""
        if not self.admin_client:
            raise ValueError("Service key 未設定，無法取得管理員客戶端")
        return self.admin_client
      # 用戶管理方法
    def create_user(self, email: str, username: str, password_hash: str, salt: str = None) -> Optional[Dict[str, Any]]:
        """建立新用戶"""
        try:
            user_data = {
                "email": email,
                "username": username,
                "password_hash": password_hash
            }
            
            # 如果提供了 salt，則加入到資料中
            if salt:
                user_data["salt"] = salt
                
            result = self.client.table("users").insert(user_data).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            print(f"建立用戶時發生錯誤: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """透過 email 取得用戶"""
        try:
            result = self.client.table("users").select("*").eq("email", email).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            print(f"透過 email 取得用戶時發生錯誤: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """透過用戶名稱取得用戶"""
        try:
            result = self.client.table("users").select("*").eq("username", username).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            print(f"透過用戶名稱取得用戶時發生錯誤: {e}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """透過 ID 取得用戶"""
        try:
            result = self.client.table("users").select("*").eq("id", user_id).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            print(f"透過 ID 取得用戶時發生錯誤: {e}")
            return None
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """更新用戶資訊"""
        try:
            result = self.client.table("users").update(updates).eq("id", user_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"更新用戶資訊時發生錯誤: {e}")
            return False
    
    # 練習進度管理方法
    def get_user_practice_progress(self, user_id: str) -> List[Dict[str, Any]]:
        """取得用戶的所有練習進度"""
        try:
            result = self.client.table("practice_progress").select("*").eq("user_id", user_id).execute()
            return result.data or []
        except Exception as e:
            print(f"取得練習進度時發生錯誤: {e}")
            return []
    
    def get_practice_progress(self, user_id: str, practice_type: str, difficulty: str) -> Optional[Dict[str, Any]]:
        """取得特定的練習進度記錄"""
        try:
            result = self.client.table("practice_progress").select("*").eq("user_id", user_id).eq("practice_type", practice_type).eq("difficulty", difficulty).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            print(f"取得特定練習進度時發生錯誤: {e}")
            return None
    
    def update_practice_progress(self, user_id: str, practice_type: str, difficulty: str, 
                               correct_count: int, total_attempts: int, mastery_level: float) -> bool:
        """更新練習進度"""
        try:
            # 先查找是否已有記錄
            existing = self.get_practice_progress(user_id, practice_type, difficulty)
            
            if existing:
                # 更新現有記錄
                result = self.client.table("practice_progress").update({
                    "correct_count": correct_count,
                    "total_attempts": total_attempts,
                    "mastery_level": mastery_level,
                    "last_practiced": "now()"
                }).eq("id", existing["id"]).execute()
                return len(result.data) > 0
            else:
                # 建立新記錄
                result = self.client.table("practice_progress").insert({
                    "user_id": user_id,
                    "practice_type": practice_type,
                    "difficulty": difficulty,
                    "correct_count": correct_count,
                    "total_attempts": total_attempts,
                    "mastery_level": mastery_level
                }).execute()
                return len(result.data) > 0
        except Exception as e:
            print(f"更新練習進度時發生錯誤: {e}")
            return False
    
    def record_practice_attempt(self, user_id: str, practice_type: str, difficulty: str, success: bool) -> bool:
        """記錄一次練習嘗試"""
        try:
            # 取得現有進度
            progress = self.get_practice_progress(user_id, practice_type, difficulty)
            
            if progress:
                new_total = progress["total_attempts"] + 1
                new_correct = progress["correct_count"] + (1 if success else 0)
                new_mastery = (new_correct / new_total) if new_total > 0 else 0.0
                
                return self.update_practice_progress(user_id, practice_type, difficulty, 
                                                   new_correct, new_total, new_mastery)
            else:
                # 建立新的進度記錄
                correct = 1 if success else 0
                total = 1
                mastery = correct / total
                
                return self.update_practice_progress(user_id, practice_type, difficulty, 
                                                   correct, total, mastery)
        except Exception as e:
            print(f"記錄練習嘗試時發生錯誤: {e}")
            return False

# 全域實例
@st.cache_resource
def get_database_manager():
    """取得資料庫管理器實例 (快取)"""
    return SupabaseManager()

def get_supabase_client() -> Client:
    """取得 Supabase 客戶端的便利函式"""
    return get_database_manager().get_client()

def test_database_connection() -> bool:
    """測試資料庫連接的便利函式"""
    return get_database_manager().test_connection()