from log_parser import count_failed_ips, extract_ip_from_failed_line


def test_extract_ip_from_failed_line_valid() -> None:
    line = (
        "May 7 10:15:01 ubuntulab sshd[1201]: "
        "Failed password for invalid user admin from 8.8.8.8 port 54321 ssh2"
    )

    result = extract_ip_from_failed_line(line)

    assert result == "8.8.8.8"


def test_extract_ip_from_accepted_line_returns_none() -> None:
    line = (
        "May 7 10:15:09 ubuntulab sshd[1203]: "
        "Accepted password for alba from 192.168.56.1 port 50214 ssh2"
    )

    result = extract_ip_from_failed_line(line)

    assert result is None


def test_count_failed_ips() -> None:
    lines = [
        "May 7 sshd[1]: Failed password for root from 8.8.8.8 port 111 ssh2",
        "May 7 sshd[2]: Failed password for admin from 1.1.1.1 port 222 ssh2",
        "May 7 sshd[3]: Failed password for test from 8.8.8.8 port 333 ssh2",
        "May 7 sshd[4]: Accepted password for alba from 192.168.56.1 port 444 ssh2",
    ]

    result = count_failed_ips(lines)

    assert result == {
        "8.8.8.8": 2,
        "1.1.1.1": 1,
    }


def test_count_failed_ips_empty_input() -> None:
    result = count_failed_ips([])

    assert result == {}
