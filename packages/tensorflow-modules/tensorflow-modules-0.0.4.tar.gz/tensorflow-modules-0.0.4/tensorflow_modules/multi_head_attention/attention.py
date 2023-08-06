import tensorflow as tf


def scaled_dot_product_attention(q, k, v, mask=None):
    """
    アテンションの重みの計算
    q, k, vは最初の次元が一致していること
    k, vは最後から2番めの次元が一致していること
    マスクは型（パディングかルックアヘッドか）によって異なるshapeを持つが、
    加算の際にブロードキャスト可能であること
    引数：
        q: query shape == (..., seq_len_q, depth)
        k: key shape == (..., seq_len_k, depth)
        v: value shape == (..., seq_len_v, depth_v)
        mask: (..., seq_len_q, seq_len_k) にブロードキャスト可能な
                    shapeを持つ浮動小数点テンソル。既定値はNone

    戻り値：
        出力、アテンションの重み
    """

    matmul_qk = tf.matmul(q, k, transpose_b=True)   # (..., seq_len_q, seq_len_k)

    # matmul_qkをスケール
    dk = tf.cast(tf.shape(k)[-1], tf.float32)
    scaled_attention_logits = matmul_qk / tf.math.sqrt(dk)

    # マスクをスケール済みテンソルに加算
    if mask is not None:
        scaled_attention_logits += (mask * -1e9)

    # softmax は最後の軸(seq_len_k)について
    # 合計が1となるように正規化
    attention_weights = tf.nn.softmax(scaled_attention_logits, axis=-1)     # (..., seq_len_q, seq_len_k)

    output = tf.matmul(attention_weights, v)    # (..., seq_len_q, depth_v)

    return output, attention_weights
