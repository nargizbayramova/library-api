"""Mock notification adapter: writes messages to the local outbox."""

def notify(email, kind, title="", fine=None):
    if kind == "checkout":
        subject, body = "Book checked out", "You checked out " + title
    elif kind == "renew":
        subject, body = "Loan renewed", "You renewed " + title
    elif kind == "return":
        subject, body = "Book returned", "You returned " + title + ". Fine: $" + str(fine)
    elif kind == "fine_paid":
        subject, body = "Fine paid", "We received $" + str(fine)
    else:
        subject, body = "Library notice", title
    with open("outbox.txt", "a") as outbox:
        outbox.write(f"TO: {email} | SUBJECT: {subject} | BODY: {body}\n")
