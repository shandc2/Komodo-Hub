from flask import render_template, Blueprint, request, redirect, url_for, flash, g, jsonify
from database.db_commands import (
    send_message, get_user_conversations, get_messages_between_users,
    mark_conversation_as_read, delete_message_for_user,
    get_unread_message_count, search_users, get_user_by_id
)

page = Blueprint("messages", __name__, url_prefix="/messages")


@page.before_request
def require_login():
    if not g.user:
        flash("You must be logged in to access messages.", "info")
        return redirect(url_for("login.login"))


@page.route("/")
def inbox():
    conversations = get_user_conversations(g.user["user_id"])
    unread_total = get_unread_message_count(g.user["user_id"])
    return render_template(
        "messages/inbox.jinja",
        conversations=conversations,
        unread_total=unread_total
    )


@page.route("/conversation/<int:user_id>")
def conversation(user_id):
    # Mark messages as read
    mark_conversation_as_read(g.user["user_id"], user_id)
    messages = get_messages_between_users(g.user["user_id"], user_id)
    
    other_user = get_user_by_id(user_id)
    if not other_user:
        flash("User not found.", "info")
        return redirect(url_for("messages.inbox"))
    
    return render_template(
        "messages/conversation.jinja",
        messages=messages,
        other_user=other_user,
        recipient_id=user_id
    )


@page.route("/send", methods=["POST"])
def send():
    recipient_id = request.form.get("recipient_id")
    subject = request.form.get("subject", "").strip()
    body = request.form.get("body", "").strip()
    parent_id = request.form.get("parent_message_id")
    
    if not body:
        flash("Message cannot be empty.", "info")
        return redirect(request.referrer or url_for("messages.inbox"))

    if not recipient_id:
        flash("user cannot be empty.", "info")
        return redirect(request.referrer or url_for("messages.inbox"))

    
    send_message(
        g.user["user_id"],
        int(recipient_id),
        subject[:200] if subject else None,
        body,
        int(parent_id) if parent_id else None
    )
    
    flash("Message sent!", "info")
    
    if parent_id:
        return redirect(url_for("messages.conversation", user_id=recipient_id))
    return redirect(url_for("messages.inbox"))


@page.route("/delete/<int:message_id>", methods=["POST"])
def delete(message_id):
    delete_message_for_user(message_id, g.user["user_id"])
    flash("Message deleted.", "info")
    return redirect(request.referrer or url_for("messages.inbox"))


@page.route("/unread-count")
def unread_count():
    if not g.user:
        return jsonify({"count": 0})
    count = get_unread_message_count(g.user["user_id"])
    return jsonify({"count": count})


@page.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if len(query) < 2:
        return jsonify({"users": []})
    
    users = search_users(query, g.user["user_id"])
    return jsonify({"users": users})


@page.route("/compose")
def compose():
    recipient_id = request.args.get("to")
    recipient_username = None
    
    if recipient_id:
        user = get_user_by_id(recipient_id)
        if user:
            recipient_username = user["username"]
    
    return render_template(
        "messages/compose.jinja",
        recipient_id=recipient_id,
        recipient_username=recipient_username
    )
