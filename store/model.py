@dataclass
class Note:
    title: str                 
    tags: List[str]            
    cipher: str                
    params: Dict[str, str]     
    ciphertext_b64: str        
    created_at: str            
