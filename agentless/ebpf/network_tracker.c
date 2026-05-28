#include "vmlinux.h"
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

char LICENSE[] SEC("license") = "GPL";

struct conn_event {
    u32 pid;
    u32 saddr;
    u32 daddr;
    u16 sport;
    u16 dport;
    u8 type;
};

struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 512 * 1024);
} conn_events SEC(".maps");

SEC("kprobe/tcp_connect")
int kprobe_tcp_connect(struct pt_regs *ctx) {
    struct sock *sk = (struct sock *)PT_REGS_PARM1(ctx);
    struct conn_event *e = bpf_ringbuf_reserve(&conn_events, sizeof(struct conn_event), 0);
    if (!e) return 0;
    e->pid = bpf_get_current_pid_tgid() >> 32;
    e->saddr = sk->__sk_common.skc_rcv_saddr;
    e->daddr = sk->__sk_common.skc_daddr;
    e->sport = bpf_ntohs(sk->__sk_common.skc_num);
    e->dport = bpf_ntohs(sk->__sk_common.skc_dport);
    e->type = 1;
    bpf_ringbuf_submit(e, 0);
    return 0;
}
