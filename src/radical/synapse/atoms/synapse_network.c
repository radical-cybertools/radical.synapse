
#include <arpa/inet.h>
#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define CHUNKSIZE  (1024 * 1024)  /* 2^20 */
 
int server        (int   port );
int server_accept (int   ssock);
int client        (char* host, int port);

int _atom_network (const char* type, const char* mode, const char* host, int port, long size)
{
  size_t n = size * CHUNKSIZE;
  char*  c = malloc (CHUNKSIZE);

  /* make sure the memory actually got allocated */
  unsigned long int i = 0;
  for ( i = 0; i < CHUNKSIZE; i++ ) {
    c[i] = '\0';
  }

  int sock = -1;

  if ( ! strcmp ("server", type) ) {
    sock = server (port);
  } else {
    sock = client (host, port);
  }


  size_t  total = 0;
  while ( total < n )
  {
    ssize_t ret = 0;

    if ( ! strcmp ("read", mode) )
    {
      while ( ret <= 0 )
      {
     // fprintf (stdout, ".");
     // fflush  (stdout);

        ret = recv (sock, c, CHUNKSIZE, MSG_WAITALL);

        if ( ret != CHUNKSIZE )
        {
          if ( errno != EAGAIN      &&
               errno != EWOULDBLOCK )
          {
            perror ("recv failed");
            exit (-1);
          }  
        }
      }
      total += ret;
    }

    else
    {
      while ( ret <= 0 )
      {
     // fprintf (stdout, ":");
     // fflush  (stdout);
        
        ret = send (sock, c, CHUNKSIZE, 0);

        if ( ret != CHUNKSIZE ) 
        {
          perror ("send failed");
          exit (-1);
        }  
      }
      total += ret;
    }
  }

  /* client closes the connection, and server waits until that is done.  This
   * way, the socket will not end up in TIME_WAIT, so we'll avoid the dreaded
   * 'Address already in use' error... */
  if ( strcmp ("server", type) ) 
  {
    close (sock);
  } 
  else 
  {
    ssize_t ret = recv (sock, c, CHUNKSIZE, MSG_WAITALL);
    /* ignore error */
  }

  return 0;

}

/* -------------------------------------------------------------------------- */
int server (int port)
{
  // printf ("creating server: %d\n", port);
  /* see http://en.wikibooks.org/wiki/C_Programming/Networking_in_UNIX */
  struct sockaddr_in dest;
  struct sockaddr_in serv;
  int    ssock;
  int    ret;
  int    opt = 1;

  memset (&serv, 0, sizeof (serv));
  serv.sin_family      = AF_INET;
  serv.sin_addr.s_addr = htonl (INADDR_ANY);
  serv.sin_port        = htons (port);

  ssock = socket (AF_INET, SOCK_STREAM, 0);
  if ( ssock < 0 ) 
  {
    perror ("socket failed");
    exit (-1);
  }  

  /* bind serv information to ssock */
  ret = bind (ssock, (struct sockaddr *)&serv, sizeof (struct sockaddr));
  if ( ret < 0 ) 
  {
    perror ("bind failed");
    exit (-1);
  }  

  /* make sure socket closes quickly on failure */
  ret = setsockopt (ssock, SOL_SOCKET, SO_REUSEADDR, (const char *)&opt, sizeof (int));
  if ( ret < 0 ) 
  {
    perror ("setsockopt failed");
    exit (-1);
  }  

  /* start listening, allowing a queue of up to 1 pending connection */
  ret = listen (ssock, 100);
  if ( ret < 0 ) 
  {
    perror ("listen failed");
    exit (-1);
  }  

  signal(SIGPIPE, SIG_IGN);

  return server_accept (ssock);
}

int server_accept (int ssock)
{
  // printf ("server accepts\n");
  struct    sockaddr_in dest;
  socklen_t socksize = sizeof (struct sockaddr_in);

  int sock = accept (ssock, (struct sockaddr *)&dest, &socksize);
  if ( sock < 0 ) 
  {
    perror ("accept failed");
    exit (-1);
  }  

  // printf ("Incoming connection from %s\n", inet_ntoa (dest.sin_addr));

  return sock;
}


/* -------------------------------------------------------------------------- */
int client (char* host, int port)
{
  // printf ("creating client: %s %d\n", host, port);
  struct sockaddr_in   addr_server;
  struct hostent     * he_server;
  int                  sock;
  int                  ret;

  sock = socket (AF_INET, SOCK_STREAM, 0);
  if ( sock < 0 ) 
  {
    perror ("cannot open socket");
    exit (-1);
  }

  he_server = gethostbyname (host);
  if ( he_server == NULL ) 
  {
    perror ("no such host");
    exit (-1);
  }

  bzero ((char *) &addr_server, sizeof(addr_server));
  bcopy ((char *) he_server->h_addr, 
         (char *) &addr_server.sin_addr.s_addr,
                  he_server->h_length);
  addr_server.sin_family = AF_INET;
  addr_server.sin_port   = htons (port);

  ret = connect (sock, (struct sockaddr *) &addr_server, sizeof(addr_server));
  if ( ret < 0 )
  {
    perror ("connect failed");
    exit (-1);
  }

  signal(SIGPIPE, SIG_IGN);

  return sock;
}

