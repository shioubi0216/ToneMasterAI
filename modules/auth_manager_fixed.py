import hashlib
import secrets
import re
import streamlit as st
from typing import Optional, Dict, Any
from modules.database import SupabaseManager

class AuthManager:
    """Manages user authentication including registration, login, and session management"""
    
    def __init__(self, db_manager: SupabaseManager):
        """Initialize with database manager"""
        self.db_manager = db_manager
    
    def hash_password(self, password: str, salt: Optional[str] = None) -> tuple[str, str]:
        """Hash password with salt
        
        Args:
            password: Plain text password
            salt: Optional salt (generates new one if None)
            
        Returns:
            Tuple of (hashed_password, salt)
        """
        if salt is None:
            salt = secrets.token_hex(32)
        
        # Combine password and salt, then hash
        password_salt = f"{password}{salt}"
        hashed = hashlib.sha256(password_salt.encode()).hexdigest()
        
        return hashed, salt
    
    def verify_password(self, password: str, hashed_password: str, salt: str) -> bool:
        """Verify password against stored hash
        
        Args:
            password: Plain text password to verify
            hashed_password: Stored hashed password
            salt: Stored salt
            
        Returns:
            True if password matches, False otherwise
        """
        hashed, _ = self.hash_password(password, salt)
        return hashed == hashed_password
    
    def validate_email(self, email: str) -> bool:
        """Validate email format
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid email format, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_username(self, username: str) -> bool:
        """Validate username format
        
        Args:
            username: Username to validate
            
        Returns:
            True if valid username format, False otherwise
        """
        # Username should be 3-20 characters, alphanumeric and underscore only
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return re.match(pattern, username) is not None
    
    def validate_password(self, password: str) -> tuple[bool, str]:
        """Validate password strength
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "密碼必須至少 8 個字元"
        
        if not re.search(r'[A-Z]', password):
            return False, "密碼必須包含至少一個大寫字母"
        
        if not re.search(r'[a-z]', password):
            return False, "密碼必須包含至少一個小寫字母"
        
        if not re.search(r'\d', password):
            return False, "密碼必須包含至少一個數字"
        
        return True, ""
    
    def register_user(self, email: str, username: str, password: str) -> tuple[bool, str, Optional[Dict]]:
        """Register a new user - 不使用 salt 欄位以避免資料庫錯誤
        
        Args:
            email: User's email address
            username: User's username
            password: User's password
            
        Returns:
            Tuple of (success, message, user_data)
        """
        # Validate inputs
        if not self.validate_email(email):
            return False, "無效的 email 格式", None
        
        if not self.validate_username(username):
            return False, "使用者名稱必須為 3-20 個字元，只能包含字母、數字和底線", None
        
        is_valid_password, password_error = self.validate_password(password)
        if not is_valid_password:
            return False, password_error, None
        
        # Check if email already exists
        existing_user = self.db_manager.get_user_by_email(email)
        if existing_user:
            return False, "此 email 已經被註冊", None
        
        # Check if username already exists
        existing_user = self.db_manager.get_user_by_username(username)
        if existing_user:
            return False, "此使用者名稱已經被使用", None
        
        # 為了避免資料庫錯誤，暫時使用簡單的密碼雜湊（不使用 salt）
        # 之後可以在 Supabase 中新增 salt 欄位後再改回加鹽雜湊
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Create user in database (不傳遞 salt)
        user_data = self.db_manager.create_user(email, username, hashed_password)
        
        if user_data:
            return True, "註冊成功！", user_data
        else:
            return False, "註冊失敗，請稍後再試", None
    
    def login_user(self, email: str, password: str) -> tuple[bool, str, Optional[Dict]]:
        """Login user with email and password
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            Tuple of (success, message, user_data)
        """
        # Validate email format
        if not self.validate_email(email):
            return False, "無效的 email 格式", None
        
        # Get user from database
        user_data = self.db_manager.get_user_by_email(email)
        
        if not user_data:
            return False, "找不到此使用者", None
        
        # Verify password
        # 檢查是否有 salt 欄位（向後相容性）
        if 'salt' in user_data and user_data['salt']:
            # 新的加鹽密碼驗證
            password_valid = self.verify_password(password, user_data['password_hash'], user_data['salt'])
        else:
            # 舊的不加鹽密碼驗證（簡單 hash 比較）
            simple_hash = hashlib.sha256(password.encode()).hexdigest()
            password_valid = simple_hash == user_data['password_hash']
        
        if password_valid:
            # Remove sensitive data before returning
            safe_user_data = {
                'id': user_data['id'],
                'email': user_data['email'],
                'username': user_data['username'],
                'created_at': user_data['created_at'],
                'updated_at': user_data['updated_at']
            }
            return True, "登入成功！", safe_user_data
        else:
            return False, "密碼錯誤", None
    
    def set_session_user(self, user_data: Dict[str, Any]) -> None:
        """Set user data in Streamlit session
        
        Args:
            user_data: User data dictionary
        """
        st.session_state['user'] = user_data
        st.session_state['logged_in'] = True
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current logged in user from session
        
        Returns:
            User data dictionary if logged in, None otherwise
        """
        if 'logged_in' in st.session_state and st.session_state['logged_in']:
            return st.session_state.get('user')
        return None
    
    def is_logged_in(self) -> bool:
        """Check if user is currently logged in
        
        Returns:
            True if user is logged in, False otherwise
        """
        return st.session_state.get('logged_in', False)
    
    def logout_user(self) -> None:
        """Logout current user by clearing session"""
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        # Ensure logged_in is False
        st.session_state['logged_in'] = False
    
    def get_user_id(self) -> Optional[str]:
        """Get current user's ID
        
        Returns:
            User ID if logged in, None otherwise
        """
        user = self.get_current_user()
        return user['id'] if user else None
    
    def update_user_profile(self, user_id: str, **kwargs) -> tuple[bool, str]:
        """Update user profile data
        
        Args:
            user_id: User's ID
            **kwargs: Fields to update
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # If updating username, validate it
            if 'username' in kwargs:
                if not self.validate_username(kwargs['username']):
                    return False, "無效的使用者名稱格式"
                
                # Check if new username already exists (excluding current user)
                existing_user = self.db_manager.get_user_by_username(kwargs['username'])
                if existing_user and existing_user['id'] != user_id:
                    return False, "此使用者名稱已經被使用"
            
            # Update user in database
            updated_user = self.db_manager.update_user(user_id, kwargs)
            
            if updated_user:
                # Update session with new data
                if self.is_logged_in():
                    current_user = self.get_current_user()
                    current_user.update(kwargs)
                    self.set_session_user(current_user)
                
                return True, "個人資料更新成功"
            else:
                return False, "更新失敗，請稍後再試"
                
        except Exception as e:
            return False, f"更新時發生錯誤：{str(e)}"
    
    def change_password(self, user_id: str, current_password: str, new_password: str) -> tuple[bool, str]:
        """Change user password
        
        Args:
            user_id: User's ID
            current_password: Current password for verification
            new_password: New password
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Get user data to verify current password
            user_data = self.db_manager.get_user_by_id(user_id)
            if not user_data:
                return False, "找不到使用者"
            
            # Verify current password (向後相容檢查)
            if 'salt' in user_data and user_data['salt']:
                password_valid = self.verify_password(current_password, user_data['password_hash'], user_data['salt'])
            else:
                simple_hash = hashlib.sha256(current_password.encode()).hexdigest()
                password_valid = simple_hash == user_data['password_hash']
                
            if not password_valid:
                return False, "當前密碼錯誤"
            
            # Validate new password
            is_valid, error_message = self.validate_password(new_password)
            if not is_valid:
                return False, error_message
            
            # Hash new password (簡單雜湊，不使用 salt)
            new_hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            
            # Update password in database
            updated_user = self.db_manager.update_user(
                user_id, 
                {"password_hash": new_hashed_password}
            )
            
            if updated_user:
                return True, "密碼更新成功"
            else:
                return False, "密碼更新失敗，請稍後再試"
                
        except Exception as e:
            return False, f"更新密碼時發生錯誤：{str(e)}"

# Global auth manager instance
_auth_manager_instance = None

def get_auth_manager():
    """Get singleton instance of AuthManager"""
    global _auth_manager_instance
    if _auth_manager_instance is None:
        from modules.database import get_database_manager
        db_manager = get_database_manager()
        _auth_manager_instance = AuthManager(db_manager)
    return _auth_manager_instance
