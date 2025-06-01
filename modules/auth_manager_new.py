"""
用戶認證管理模組
處理用戶註冊、登入、登出功能
"""

import hashlib
import secrets
import re
from typing import Optional, Dict, Any, Tuple
from modules.database import get_database_manager
import streamlit as st

class AuthManager:
    """用戶認證管理類別"""
    
    def __init__(self):
        """初始化認證管理器"""
        self.db = get_database_manager()
        
    def hash_password(self, password: str) -> str:
        """加密密碼"""
        # 使用 SHA-256 加密密碼
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{password_hash}"
    
    def verify_password(self, password: str, stored_hash: str) -> bool:
        """驗證密碼"""
        try:
            salt, password_hash = stored_hash.split(':')
            test_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return test_hash == password_hash
        except ValueError:
            return False
    
    def validate_email(self, email: str) -> bool:
        """驗證 email 格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_username(self, username: str) -> bool:
        """驗證用戶名稱格式"""
        # 用戶名稱只能包含字母、數字和底線，長度 3-20
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return bool(re.match(pattern, username))
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
        """驗證密碼強度"""
        if len(password) < 6:
            return False, "密碼長度至少需要 6 個字符"
        if len(password) > 128:
            return False, "密碼長度不能超過 128 個字符"
        return True, ""
    
    def register_user(self, email: str, username: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """註冊新用戶"""
        try:
            # 驗證輸入格式
            if not self.validate_email(email):
                return False, "請輸入有效的 email 地址", None
            
            if not self.validate_username(username):
                return False, "用戶名稱只能包含字母、數字和底線，長度 3-20 字符", None
            
            is_valid_password, password_error = self.validate_password(password)
            if not is_valid_password:
                return False, password_error, None
            
            # 檢查 email 是否已存在
            existing_email = self.db.get_user_by_email(email)
            if existing_email:
                return False, "此 email 已被註冊", None
            
            # 檢查用戶名稱是否已存在
            existing_username = self.db.get_user_by_username(username)
            if existing_username:
                return False, "此用戶名稱已被使用", None
            
            # 加密密碼
            password_hash = self.hash_password(password)
            
            # 建立用戶
            user = self.db.create_user(email, username, password_hash)
            if user:
                return True, "註冊成功！", user
            else:
                return False, "註冊失敗，請稍後再試", None
                
        except Exception as e:
            print(f"註冊用戶時發生錯誤: {e}")
            return False, "註冊失敗，系統錯誤", None
    
    def login_user(self, email_or_username: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """用戶登入"""
        try:
            # 檢查是否為 email 格式
            if '@' in email_or_username:
                user = self.db.get_user_by_email(email_or_username)
            else:
                user = self.db.get_user_by_username(email_or_username)
            
            if not user:
                return False, "用戶不存在", None
            
            # 驗證密碼
            if not user.get('password_hash'):
                return False, "用戶帳號異常，請聯繫管理員", None
            
            if self.verify_password(password, user['password_hash']):
                return True, "登入成功！", user
            else:
                return False, "密碼錯誤", None
                
        except Exception as e:
            print(f"用戶登入時發生錯誤: {e}")
            return False, "登入失敗，系統錯誤", None
    
    def logout_user(self) -> None:
        """用戶登出"""
        # 清除 session 中的用戶資訊
        if 'user' in st.session_state:
            del st.session_state['user']
        if 'user_id' in st.session_state:
            del st.session_state['user_id']
        if 'logged_in' in st.session_state:
            del st.session_state['logged_in']
        if 'remember_me' in st.session_state:
            del st.session_state['remember_me']
    
    def is_logged_in(self) -> bool:
        """檢查用戶是否已登入"""
        return st.session_state.get('logged_in', False) and st.session_state.get('user_id') is not None
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """取得當前登入的用戶資訊"""
        if self.is_logged_in():
            return st.session_state.get('user')
        return None
    
    def get_current_user_id(self) -> Optional[str]:
        """取得當前登入的用戶 ID"""
        if self.is_logged_in():
            return st.session_state.get('user_id')
        return None
    
    def set_session(self, user: Dict[str, Any], remember_me: bool = False) -> None:
        """設定用戶 session"""
        st.session_state['logged_in'] = True
        st.session_state['user'] = user
        st.session_state['user_id'] = user['id']
        st.session_state['remember_me'] = remember_me
    
    def change_password(self, current_password: str, new_password: str) -> Tuple[bool, str]:
        """更改密碼"""
        try:
            user = self.get_current_user()
            if not user:
                return False, "請先登入"
            
            # 驗證當前密碼
            if not self.verify_password(current_password, user['password_hash']):
                return False, "當前密碼錯誤"
            
            # 驗證新密碼
            is_valid, error_msg = self.validate_password(new_password)
            if not is_valid:
                return False, error_msg
            
            # 更新密碼
            new_password_hash = self.hash_password(new_password)
            success = self.db.update_user(user['id'], {'password_hash': new_password_hash})
            
            if success:
                # 更新 session 中的用戶資訊
                user['password_hash'] = new_password_hash
                st.session_state['user'] = user
                return True, "密碼更新成功"
            else:
                return False, "密碼更新失敗"
                
        except Exception as e:
            print(f"更改密碼時發生錯誤: {e}")
            return False, "系統錯誤，請稍後再試"

# 全域實例
@st.cache_resource
def get_auth_manager():
    """取得認證管理器實例 (快取)"""
    return AuthManager()
