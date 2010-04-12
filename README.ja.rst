Jogging は Django でのロギングを簡単にするための、Python の logging のラッパです。
これはすべてのロガーの設定を一箇所でできるようにし、ロガーをインポートする標準の場所の提供や、一般的なロギングユースケースを簡潔にすることができます。

Jogging を使えば、保存場所やフォーマット、適切な粒度の詳細ログの管理が可能です。
モジュールレベルのロギング設定も、特定の関数のロギング設定のように簡単に実現できます。

使用するには、settings.py に数行設定を追加し、Python のログ関数の変りに Jogging のログ関数をインポートします。そしていつものようにログを取るだけです。

Python の logging モジュールが全ての重要な処理を担っているため、Jogging から既に存在するコードのロギングの設定を行なうことができます。
また抽象化によって logging の威力が損なわれないようにしています。


============
ダウンロード
============

最新リリース版 (2009/10/27 リリースの v0.1)を `ダウンロード <http://github.com/zain/jogging/downloads>`_ セクションから取得できます。


============
インストール
============

1. ``INSTALLED_APPS`` に ``'jogging'`` を追加
2. ``MIDDLEWARE_CLASSES`` に ``'jogging.middleware.LoggingMiddleware'`` を追加


====
設定
====

言葉で説明するよりコードサンプルの方が簡単なので、いくつかのサンプルを載せます。
これらを settings.py に記述して下さい。


基本的な設定例
--------------

::

    from jogging.handlers import DatabaseHandler
    import logging

    GLOBAL_LOG_LEVEL = logging.INFO
    GLOBAL_LOG_HANDLERS = [DatabaseHandler()] # takes any Handler object that Python's logging takes

INFO レベル以上のログがデータベースへ保存されます。

Jogging はハンドラをラップしないことに注意して下さい; ハンドラは logging と同様のオブジェクトです。
これは logging.Hander でできることは全てできる、ということであり、Jogging にハンドラオブジェクトを渡すことができる、ということです。


中間的な設定例
--------------

::

    from jogging.handlers import DatabaseHandler
    from logging import StreamHandler
    import logging

    LOGGING = {
        # myapp1 の全てのログをデータベースに
        'myapp1': {
            'handler': DatabaseHandler(), # an initialized handler object
            'level': logging.DEBUG,
        },
    
        # ... この view だけは stderr に CRITICAL なログを吐く
        'myapp1.views.super_important_view': {
            'handler': StreamHandler(),
            'level': logging.CRITICAL,
        },
    }

特定のロガーだけにマッチします(この例では ``super_important_view()`` ではデータベースにログを残しません)


高度な設定例
------------

::

    from jogging.handlers import DatabaseHandler
    from logging import StreamHandler, FileHandler
    import logging

    LOGGING = {
        # myapp1 の全てのログをデータベースに
        'myapp1': {
            'handler': DatabaseHandler(),
            'level': logging.DEBUG,
        },
    
        # 今回も super_important_view だけ CRITICAL なログを stderr に吐くが、
        # それ以外のレベルのログはデータベースに吐く
        'myapp1.views.super_important_view': {
            'handlers': [
                { 'handler': StreamHandler(), 'level': logging.CRITICAL, 
                    'format': "%(asctime)-15s %(source): %(message)s %(foo)s" },
                { 'handler': DatabaseHandler(), 'level': logging.DEBUG },
            ]
        },
    
        # サードパーティのアプリにおいて、既にログをとっている場合のロガー名。
        # これも他の設定と同様に記述できる。
        'simple_example': {
            'handler': StreamHandler(),
            'level': logging.CRITICAL,
        }
    }

ハンドラのフォーマットプロパティは Python の logging の書式化文字列に加え、以下の拡張文字列があります:

- ``%(source)s`` はロギング呼び出し元のメソッド
- ``%(foo)s`` はロギング呼び出し時に渡されたパラメータ


=====
Usage
=====

::

    from jogging import logging
    logging.info("I'm an info message")
    logging.debug(msg="I'm a debug message", foo="bar")

``%(foo)s`` は上記の高度な例で言及した ``'format'`` プロパティにあったということを覚えてるでしょうか？
これはデバッグ呼び出し時には ``"bar"`` として与えられます。


================
カスタムハンドラ
================

``jogging.handlers.DatabaseHandler``
  データベースにログを保存し、管理画面において閲覧/検索/絞り込みが可能になります。

``jogging.handlers.EmailHandler``
  ログをEメールで送信します。

``jogging.handlers.InlineOnPageHandler``
  作成予定。レンダーしたページの下部にログを表示します。


===
FAQ
===

Jogging と django-logging の違いは？
    Djagno logging は単一のルートロガーを提供しますが、Jogging は異なるモジュールで異なるロガーを使うことができます。
    上述の "基本的な設定例" のように設定することで、django-logging の同じような使い方ができます。

Jogging と django-db-log の違いは？
    django-db-log は例外のログをデータベースに保存してくれるだけです。
    これはデバッグや一般的なロギングの目的には合っていませんし、Python の logging モジュールで提供するような機能は何もありません。
    Jogging は DatabaseHandler というハンドラを使えば、django-db-log のように例外ログ(だけでなくなんでも)データベースへ保存することができます。

logging の log 関数と Jogging を併用できるか？また Jogging の log 関数を使ったほうがいい理由は？
    二つの理由があります: まずひとつめは、ロガーのフォーマッタにおいて、呼び出し関数名として ``source`` 変数を使うことができます。
    ふたつめは、Jogging の log 関数は自動的に正しいロガーを選択するため、どのロガーが設定されているのか気にする必要がありません。


============
実装について
============

`Django's logging proposal <http://groups.google.com/group/django-developers/browse_thread/thread/8551ecdb7412ab22>`_ から多大なインスピレーションを受けています。

Jogging は Jogging によって管理するロガーの(名前の)定義辞書 ``settings.LOGGING`` の設定が必要です。Jogging の動作は:

1. 全てのロガーはサーバの起動時に ``settings.LOGGING`` から作成されます
   (初期化コードは、ちょうどいい場所がなかったので、ミドルウェア内の ``__init__`` にしています)。
   ハンドラは定義通りにロガーに追加され、ログレベルがセットされます。
2. アプリケーションが Jogging の log 関数を呼び出す際、呼び出し元の関数は ``settings.LOGGING`` で設定されたロガー名から
   合ったものを探し、より具体的なロガー名が選択されます。
   例えば、呼び出し元を ``myproj.myapp.views.func()`` とした場合、次の名前のロガーからマッチするロガー名を探します。 ``myproj.myapp.views.func``, ``myproj.myapp.views``, ``myproj.myapp``, ``myproj`` 。
   この場合、最初の(そしてより具体的な)ロガーがマッチして選択されます。
3. ``log()`` は選択されたロガーから呼び出され、Python の logging モジュールに渡されます。


========
リソース
========

Python logging モジュールのハンドラ一覧:
http://docs.python.org/library/logging.html#handler-objects

Python loggign モジュールの書式化文字列:
http://docs.python.org/library/logging.html#formatter-objects


====
ToDo
====

- Instantiate handlers outside of settings.py (e.g. so the ORM can be used)
- settings.py より外でハンドラのインスタンス化を行なうようにする(例えば ORM で使えるように)
- もっとカスタムハンドラを作成する


============
名前について
============

最初の "j" は発音せずに "ヨギング" と読みます。
