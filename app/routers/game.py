from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..database import get_db
from ..models import Room
from ..game.logic import Gomoku
from ..game.ai import get_ai_move

router = APIRouter()
room_states = {}


@router.post("/rooms/{room_id}/move")
def make_move(room_id: int, x: int, y: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room or not room.is_started:
        raise HTTPException(status_code=404, detail="房间不存在或未开始")

    # 创建房间状态
    if room_id not in room_states:
        room_states[room_id] = Gomoku()

    game = room_states[room_id]
    player_id = 1 if user.id == room.owner_id else 2

    if not game.make_move(x, y, player_id):
        raise HTTPException(status_code=400, detail="非法落子")

    result = {
        "board": game.board,
        "moves": game.moves,
        "winner": game.winner,
    }

    # 如果对手是AI
    if room.player2_id is None and game.winner is None:
        ax, ay = get_ai_move(game.board)
        game.make_move(ax, ay, 2)
        result["moves"] = game.moves
        result["board"] = game.board
        result["winner"] = game.winner

    return result
