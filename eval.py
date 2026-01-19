import chess
from fork import fork_score
from pin import pin_score
from en_passant import en_passant_score
from castling import castling_score
from development import development_score

# Basic piece values for scoring captures and hanging pieces
piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

def evaluate_board(board):
    """
    Full Clownfish evaluation function.
    Combines piece safety, tactical bonuses, development, castling, forks, pins, en passant, and checks.
    """

    score = 0.0

    # 1️⃣ Piece safety and capture bonuses
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            # Penalize hanging pieces (attacked without defenders)
            if board.is_attacked_by(not piece.color, square) and not board.is_attacked_by(piece.color, square):
                score -= 0.4 * value
            # Bonus for defending pieces
            if board.is_attacked_by(piece.color, square):
                score += 0.3
            # Bonus for capturing pieces (approximation, added for AI weighting)
            if board.is_attacked_by(not piece.color, square):
                score += 0.3 * value

    # 2️⃣ Castling bonus
    score += castling_score(board)

    # 3️⃣ King safety: reduce score for moves into check squares
    king_sq = board.king(board.turn)
    if king_sq is not None:
        king_moves = list(board.attacks(king_sq))
        for move_sq in king_moves:
            if board.is_attacked_by(not board.turn, move_sq):
                score -= 0.2

    # 4️⃣ Forks
    score += fork_score(board)

    # 5️⃣ Pins
    score += pin_score(board)

    # 6️⃣ En passant
    score += en_passant_score(board)

    # 7️⃣ Development bonus
    score += development_score(board)

    # 8️⃣ Check bonus
    if board.is_check():
        score += 0.5

    # 9️⃣ Checkmate: infinite score
    if board.is_checkmate():
        # If it's white's turn and checkmated, negative infinity
        score = float('inf') if board.turn == chess.BLACK else -float('inf')

    # Return score relative to current player
    return score if board.turn == chess.WHITE else -score
